'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from itertools import permutations, combinations
from constants import *
from utils import *
from core import *
from moba2 import *
from btnode import *

###########################
### SET UP BEHAVIOR TREE


def treeSpec(agent):
	myid = str(agent.getTeam())
	spec = None
	### YOUR CODE GOES BELOW HERE ###

	### YOUR CODE GOES ABOVE HERE ###
	return spec

def myBuildTree(agent):
	myid = str(agent.getTeam())
	root = None
	### YOUR CODE GOES BELOW HERE ###
	# Start from leaf nodes

	dodge = makeNode(Dodge, agent)
	retreat = makeNode(Retreat, agent, 0.75)
	aoe_daemon = makeNode(AOEDaemon, agent)
	aoe_selector = makeNode(Selector, agent, 'aoe_selector')
	aoe_hero = makeNode(AOEHero, agent)
	aoe_minion = makeNode(AOEMinion, agent)
	shoot_daemon = makeNode(ShootDaemon, agent)
	shoot_selector = makeNode(Selector, agent, 'shoot_selector')
	shoot_hero = makeNode(ShootHero, agent)
	shoot_minion = makeNode(ShootMinion, agent)
	hp_daemon = makeNode(HitpointDaemon, agent)
	chase_selector = makeNode(Selector, agent, 'chase_selector')
	lvl_daemon = makeNode(BuffDaemon, agent)
	chase_hero = makeNode(ChaseHero, agent)
	chase_minion = makeNode(ChaseMinion, agent)

	root = makeNode(Selector, agent, 'root')

	root.addChild(dodge)
	root.addChild(retreat)
	# root.addChild(aoe_daemon)
	root.addChild(shoot_daemon)
	root.addChild(hp_daemon)

	aoe_daemon.addChild(aoe_selector)

	shoot_daemon.addChild(shoot_selector)

	hp_daemon.addChild(chase_selector)

	aoe_selector.addChild(aoe_hero)
	aoe_selector.addChild(aoe_minion)

	shoot_selector.addChild(shoot_hero)
	shoot_selector.addChild(shoot_minion)

	chase_selector.addChild(lvl_daemon)
	chase_selector.addChild(chase_minion)

	lvl_daemon.addChild(chase_hero)

	### YOUR CODE GOES ABOVE HERE ###
	return root

### Helper function for making BTNodes (and sub-classes of BTNodes).
### type: class type (BTNode or a sub-class)
### agent: reference to the agent to be controlled
### This function takes any number of additional arguments that will be passed to the BTNode and parsed using BTNode.parseArgs()
def makeNode(type, agent, *args):
	node = type(agent, args)
	return node

###############################
### BEHAVIOR CLASSES:


##################
### Taunt
###
### Print disparaging comment, addressed to a given NPC
### Parameters:
###   0: reference to an NPC
###   1: node ID string (optional)

class Taunt(BTNode):

	### target: the enemy agent to taunt

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		# First argument is the target
		if len(args) > 0:
			self.target = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target is not None:
			print "Hey", self.target, "I don't like you!"
		return ret

##################
### MoveToTarget
###
### Move the agent to a given (x, y)
### Parameters:
###   0: a point (x, y)
###   1: node ID string (optional)

class MoveToTarget(BTNode):
	
	### target: a point (x, y)
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		# First argument is the target
		if len(args) > 0:
			self.target = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def enter(self):
		BTNode.enter(self)
		self.agent.navigateTo(self.target)

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target == None:
			# failed executability conditions
			# print "exec", self.id, "false"
			return False
		elif distance(self.agent.getLocation(), self.target) < self.agent.getRadius():
			# Execution succeeds
			# print "exec", self.id, "true"
			return True
		else:
			# executing
			return None
		return ret

# Find list of nodes within the radius of a provided point
def getPointInRadius(p, r_out, r_inner, possibleDests):
	points = filter(lambda x, p=p, r_out=r_out, r_inner=r_inner: distance(x,p) <= r_out and distance(x,p) >= r_inner, possibleDests)
	# print points
	return points[np.random.choice(len(points), 1)[0]]

def angleDegrees(p1, p2):
	ang = angle(p1, p2) * 360/(2*math.pi)
	# Third and fourth quadrent, negative
	if p2[1] < 0:
		ang *= -1
	return ang

# Find a point that is movable and away from a bullet
def getValidAngle(p, r, bullet_pos, possibleDests):
	x_axis = (1,0)
	# Get relative position
	bullet_pos = (bullet_pos[0] - p[0], bullet_pos[1] - p[1])
	# print bullet_pos
	# Get relative angle
	bullet_angle = angleDegrees(x_axis, bullet_pos)
	# print bullet_angle
	# Get relative points movable to
	mvmt_pts = [(pnt[0] - p[0], pnt[1] - p[1]) for pnt in possibleDests if distance(pnt,p) <= r + 1 and distance(pnt,p) >= r - 1]
	# print mvmt_pts
	# Find angles able to be moved to
	angles = [angleDegrees(x_axis, p2) for p2 in mvmt_pts if abs(angleDegrees(x_axis, p2)) >= bullet_angle + 25 or abs(angleDegrees(x_axis, p2)) <= bullet_angle - 25]
	# angles = [angleDegrees(x_axis, p2) for p2 in mvmt_pts]
	# print angles
	if angles:
		return angles[np.random.choice(len(angles), 1)[0]]
	else:
		return None

##################
### Dodge
###
### Move the agent back to the base to be healed
### Parameters:
###   0: Angle to dodge at (optional)
###   1: node ID string (optional)


class Dodge(BTNode):
	
	### angle: angle in degrees at which to dodge
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.angle = None
		self.id = "dodge"
		# First argument is the factor
		if len(args) > 0:
			self.angle = args[0] % 360
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def enter(self):
		BTNode.enter(self)
		self.bullets = [i for i in self.agent.getVisibleType(Bullet) if distance(self.agent.getLocation(), i.getLocation())]
		# print self.bullets
	
	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		# If the agent can't dodge yet or there are no bullets to dodge, return Failure
		if not self.bullets or not self.agent.canDodge():
			# print "exec", self.id, "false"
			return False
		
		# If an angle was set, jump in that direction regardless of consequence
		if self.angle:
			self.agent.dodge(self.angle)
			# print "exec", self.id, "true"
			return True

		# When no angle given manually, find the perpendicular line to the bullet,
		#  jump there only if the location is movable, also avoid exception when bullet
		#  has already hit and has yet to die
		if self.agent.getLocation() == self.bullets[0].getLocation():
			# print "exec", self.id, "false"
			return False

		# How far the agent can jump
		jmp_range = self.agent.getRadius()*1.5

		escape_angle = getValidAngle(self.agent.getLocation(), jmp_range, self.bullets[0].getLocation(), self.agent.getPossibleDestinations())

		# print escape_angle

		if escape_angle:
			self.agent.dodge(escape_angle)
			# print "exec", self.id, "true"
			return True
		else:
			# print "exec", self.id, "true"
			return False

##################
### Retreat
###
### Move the agent back to the base to be healed
### Parameters:
###   0: percentage of hitpoints that must have been lost to retreat
###   1: node ID string (optional)


class Retreat(BTNode):
	
	### percentage: Percentage of hitpoints that must have been lost
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.percentage = 0.5
		self.my_base = self.agent.world.getBaseForTeam(self.agent.getTeam()).getLocation()
		self.id = 'retreat'
		# First argument is the factor
		if len(args) > 0:
			self.percentage = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.agent.getHitpoints() >= self.agent.getMaxHitpoints() * self.percentage or \
		   self.agent.getMoveTarget() == self.my_base:
			# fail executability conditions
			# print "exec", self.id, "false"
			return False
		else:
			# Exection succeeds
			# print "exec", self.id, "true"
			self.agent.navigateTo(self.my_base)
			return True
		return ret

##################
### ChaseMinion
###
### Find the closest minion and move to intercept it.
### Parameters:
###   0: node ID string (optional)


class ChaseMinion(BTNode):

	### target: the minion to chase
	### timer: how often to replan

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		self.id = 'chase minion'
		# First argument is the node ID
		if len(args) > 0:
			self.id = args[0]

	def enter(self):
		BTNode.enter(self)

		minions = [enm for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()) if isinstance(enm, Minion)]
		for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()):
			if isinstance(enm, Hero):
				hero = enm
				break
		# TODO: Find a target minion that is furthest away from enemy hero if hero is in sight
		if minions and hero:
			self.target = max(minions, lambda x: distance(hero.getLocation(), x.getLocation()))
			if isinstance(self.target, list):
				self.target = self.target[0]
			# print "max", self.target
		elif minions:
			self.target = min(minions, lambda x: distance(self.agent.getLocation(), x.getLocation()))
			if isinstance(self.target, list):
				self.target = self.target[0]
			# print "min", self.target
		else:
			self.target = None


	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		
		# print self.agent

		if not self.target:
			# print "exec", self.id, "false"
			ret = False
		elif not self.target.isAlive() or self.agent.isMoving():
			# failed execution conditions
			# print "exec", self.id, "false"
			ret = False
		else:
			# executing
			# print "exec", self.id, "true"
			navTarget = self.chooseNavigationTarget()
			if navTarget is not None:
				self.agent.navigateTo(navTarget)
			ret = True
		return ret

	# Choose a point within attacking radius of the target's destination
	def chooseNavigationTarget(self):
		if self.target.getMoveTarget():
			tar = self.target.getMoveTarget()
		else:
			tar = self.target.getLocation()
		return getPointInRadius(tar, BULLETRANGE, 0, self.agent.getPossibleDestinations())
		

##################
### ShootMinion
###
### Shoot the closest minion. If it is already in range.
### Parameters:
###   0: node ID string (optional)


class ShootMinion(BTNode):

	### target: the minion to shoot

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		self.id = 'shoot minion'
		# First argument is the node ID
		if len(args) > 0:
			self.id = args[0]

	def enter(self):
		BTNode.enter(self)
		# print("Attacking Minion")
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if len(enemies) > 0:
			best = None
			dist = 0
			for e in enemies:
				if isinstance(e, Minion):
					d = distance(self.agent.getLocation(), e.getLocation())
					if best == None or d < dist:
						best = e
						dist = d
			self.target = best


	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if not self.agent.canFire() or self.target == None \
		or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
			# failed executability conditions
			# print "exec", self.id, "false"
			return False
		else:
			# executing
			self.shootAtTarget()
			# print "exec", self.id, "true"
			return True
		return ret

	def shootAtTarget(self):
		if self.agent is not None and self.target is not None:
			self.agent.stopMoving()
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()


##################
### ChaseHero
###
### Move to intercept the enemy Hero.
### Parameters:
###   0: node ID string (optional)

class ChaseHero(BTNode):

	### target: the minion to chase
	### timer: how often to replan

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		self.max_enemies = 10
		self.id = 'chase hero'
		# First argument is the number of allowable nearby enemies
		if len(args) > 0:
			self.max_enemies = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def enter(self):
		BTNode.enter(self)
		self.target = None
		# TODO: Find a target hero, but only do so if not near other minions
		minions = [enm for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()) if isinstance(enm, Minion)]
		for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()):
			if isinstance(enm, Hero):
				hero = enm
				break

		if minions and hero:
			if len([minion for minion in minions if distance(minion.getLocation(), hero.getLocation()) < BULLETRANGE]) <= self.max_enemies:
				self.target = hero
			else:
				self.target = None
		elif hero:
			self.target = hero
		else:
			self.target = None

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)

		if not self.target or not self.target.isAlive() or self.agent.isMoving():
			# failed execution conditions
			# print "exec", self.id, "false"
			return False
		else:
			# executing
			# print "exec", self.id, "true"
			navTarget = self.chooseNavigationTarget()
			if navTarget is not None:
				self.agent.navigateTo(navTarget)
			return True
		return ret

	# Choose a point within attacking radius of the target's destination
	def chooseNavigationTarget(self):
		if self.target.getMoveTarget():
			tar = self.target.getMoveTarget()
		else:
			tar = self.target.getLocation()
		return getPointInRadius(tar, BULLETRANGE, 0, self.agent.getPossibleDestinations())

##################
### ShootHero
###
### Shoot the enemy hero. If it is already in range.
### Parameters:
###   0: node ID string (optional)


class ShootHero(BTNode):

	### target: the minion to shoot

	def ParseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.target = None
		self.id = 'shoot hero'
		# First argument is the node ID
		if len(args) > 0:
			self.id = args[0]

	def enter(self):
		BTNode.enter(self)
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		for e in enemies:
			if isinstance(e, Hero):
				self.target = e
				return None

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
			# failed executability conditions
			# if self.target == None:
				# print " none"
			# else:
				# print "foo dist", distance(self.agent.getLocation(), self.target.getLocation())
			# print "exec", self.id, "false"
			return False
		else:
			#executing
			# print "exec", self.id, "true"
			self.shootAtTarget()
			return True
		return ret

	def shootAtTarget(self):
		if self.agent is not None and self.target is not None:
			self.agent.stopMoving()
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()


##################
### HitpointDaemon
###
### Only execute children if hitpoints are above a certain threshold.
### Parameters:
###   0: percentage of hitpoints that must have been lost to fail the daemon check
###   1: node ID string (optional)


class HitpointDaemon(BTNode):
	
	### percentage: percentage of hitpoints that must have been lost to fail the daemon check
	
	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.percentage = 0.5
		self.id = 'hp daemon'
		# First argument is the factor
		if len(args) > 0:
			self.percentage = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		if self.agent.getHitpoints() < self.agent.getMaxHitpoints() * self.percentage:
			# Check failed
			# print "exec", self.id, "fail"
			return False
		else:
			# Check didn't fail, return child's status
			# print "exec", self.id, "succeed"
			return self.getChild(0).execute(delta)
		return ret

##################
### BuffDaemon
###
### Only execute children if agent's level is significantly above enemy hero's level.
### Parameters:
###   0: Number of levels above enemy level necessary to not fail the check
###   1: node ID string (optional)

class BuffDaemon(BTNode):

	### advantage: Number of levels above enemy level necessary to not fail the check

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.advantage = 0
		self.id = 'buff daemon'
		# First argument is the advantage
		if len(args) > 0:
			self.advantage = args[0]
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		hero = None
		# Get a reference to the enemy hero
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		for e in enemies:
			if isinstance(e, Hero):
				hero = e
				break
		if hero == None or self.agent.level <= hero.level + self.advantage:
			# fail check
			# print "exec", self.id, "fail"
			return False
		else:
			# print "exec", self.id, "succeed"
			# Check didn't fail, return child's status
			return self.getChild(0).execute(delta)
		return ret

##################
### AOEDaemon
###
### Only execute children if agent's level is significantly above enemy hero's level.
### Parameters:
###   0: node ID string (optional)

class AOEDaemon(BTNode):

	### advantage: Number of levels above enemy level necessary to not fail the check

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.id = 'aoe daemon'
		if len(args) > 0:
			self.id = args[0]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)

		if self.agent.canAreaEffect():
			# print "exec", self.id, "succeed"
			return self.getChild(0).execute(delta)
		else:
			# print "exec", self.id, "fail"
			return False

##################
### ShootDaemon
###
### Only execute children if the agent is able to shoot.
### Parameters:
###   0: node ID string (optional)

class ShootDaemon(BTNode):

	def parseArgs(self, args):
		BTNode.parseArgs(self, args)
		self.id = 'shoot daemon'
		if len(args) > 0:
			self.id = args[0]

	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)

		if self.agent.canFire():
			# print "exec", self.id, "succeed"
			return self.getChild(0).execute(delta)
		else:
			# print "exec", self.id, "fail"
			return False


##################
### AOEMinion
###
### Perform AOE on minion found in daemon.
### Parameters:
###   0: node ID string (optional)


class AOEMinion(BTNode):
	### target: the minion to shoot

	def parseArgs(self, args):
		self.min_enemies = 1
		self.target = None
		self.id = 'aoe minion'
		# First argument is the minimum number of enemies surrounding
		if len(args) > 0:
			self.min_enemies = args[0]
			if self.min_enemies <= 0:
				raise ValueError('minimum number of enemies cannot be zero or lower')
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]
		
		self.aoe_range = AREAEFFECTRANGE * self.agent.getRadius()

	def enter(self):
		BTNode.enter(self)
		enemies = [enm for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()) if isinstance(enm, Minion)]

		# If a minion is within the range, don't think twice, just blast 'em
		for e in enemies:
			if distance(e.getLocation(), self.agent.getLocation()) < self.aoe_range:
				self.target = e
				return
		
		# TODO: See if there are at least min_enemies around the minion (including itself)
		enemies = permutations(enemies, self.min_enemies)
		for combo in enemies:
			for i in range(1, self.min_enemies):
				if distance(combo[0].getLocation(), combo[i].getLocation()) > self.aoe_range:
					break
			self.target = combo[0]
			return


	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		# Get list of minions in the scene
		enemies = [enm for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()) if isinstance(enm, Minion)]

		# TODO: See if there are at least min_enemies around the minion (including itself)
		count = 0
		for enm in enemies:
			if distance(self.target.getLocation(), enm.getLocation()) < self.aoe_range:
				count += 1


		# In the event the agent can't area effect or no target being available, return false
		if not self.target or \
		not distance(self.agent.getLocation(), self.target.getLocation()) >= self.aoe_range:
			# print "exec", self.id, "false"
			return False
		elif distance(self.agent.getLocation(), self.target.getLocation()) < self.aoe_range:
			self.agent.areaEffect()
			# print "exec", self.id, "true"
			return True

		return ret

##################
### AOEHero
###
### Perform AOE on minion found in daemon.
### Parameters:
###   0: node ID string (optional)


class AOEHero(BTNode):
	### target: the minion to shoot

	def parseArgs(self, args):
		self.min_enemies = 1
		self.target = None
		self.id = 'aoe hero'
		# First argument is the minimum number of enemies surrounding
		if len(args) > 0:
			self.min_enemies = args[0]
			if self.min_enemies <= 0:
				raise ValueError('minimum number of enemies cannot be zero or lower')
		# Second argument is the node ID
		if len(args) > 1:
			self.id = args[1]
		
		self.aoe_range = AREAEFFECTRANGE * self.agent.getRadius()

	def enter(self):
		BTNode.enter(self)
		for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()):
			if isinstance(enm, Hero):
				self.target = enm
				return


	def execute(self, delta = 0):
		ret = BTNode.execute(self, delta)
		# Get list of minions in the scene
		enemies = [enm for enm in self.agent.world.getEnemyNPCs(self.agent.getTeam()) if isinstance(enm, Minion)]

		# TODO: See if there are at least min_enemies around the minion (including itself)
		count = 0
		for enm in enemies:
			if distance(self.target.getLocation(), enm.getLocation()) < self.aoe_range:
				count += 1

		# In the event the agent can't area effect or no target being available, return false
		if not self.target or \
		not distance(self.agent.getLocation(), self.target.getLocation()) >= self.aoe_range \
		or count < self.min_enemies:
			# print "exec", self.id, "false"
			return False
		elif distance(self.agent.getLocation(), self.target.getLocation()) < self.aoe_range:
			self.agent.areaEffect()
			# print "exec", self.id, "true"
			return True


#################################
### MY CUSTOM BEHAVIOR CLASSES