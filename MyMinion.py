__author__ = "jacob logas"
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

from constants import *
from utils import *
from core import *
from moba import *

# Health variable used to provide friendlies information on their comrades' status
ally_health = {"healthy": [], "moderate": [], "danger": []}

# Live friendly minion count
alive = 0

# Allows for grouping of allies and coordinated attacks
squads = {'defend': [], 'backup': [], 'attacking': []}

class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		# self.states = [Idle]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		self.target = None
		# If the state has finished
		self.state_finished = True
		self.states = [Idle, Attack, Move, Pursue, Flank, Support, Defend, Dodge]
		self.squad = None
		self.moving = False
		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Move, self.squad, self.getTeam())

############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		# First check if bullets are directed at you and dodge if so
		agent = self.agent
		team = agent.getTeam()
		# TODO: Test this gets only bullets pointing at the agent
		bullets = [bullet.getTeam() != team and\
				   numpy.isclose(bullet.getOrientation(), \
				   angle(agent.getPosition(), bullet.getPosition))\
				   for bullet in agent.getVisibleType(MOBABullet)]
		enemies = [enemy.getTeam() != team and \
				   type(enemy) != MOBABullet for enemy \
				   in agent.getVisible()]
		if bullets:
			agent.changeState(Dodge, bullets)
		# Then if you have a target and its in range, attack it or pursue if not in range
		elif agent.target:
			if distance(agent.target.position, agent.position) <= BULLETRANGE:
				agent.changeState(Attack, agent.target)
			else:
				agent.changeState(Pursue, agent.target)
		# TODO: If you dont have a target, find an in-range enemy and attack closest
		elif not agent.target and enemies:
			agent.changeState(LockOn, enemies)
		# TODO: If no targets are available, MOVE!!!
		elif not enemies:
			if not agent.moving:
				agent.changeState(Move, agent.squad, agent.getTeam())
				agent.moving = True
		### YOUR CODE GOES ABOVE HERE ###
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print "Hey " + str(self.victim) + ", I don't like you!"
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:

##############################
### Attack
###
### Shoots at the minion's target
### 

class Attack(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		# TODO: Shoot at the target passed in
		if self.agent.canfire:
			self.agent.turnToFace(self.agent.target.getLocation())
			self.agent.shoot()
		pass

##############################
### Move
###
### Move to the given position
### interruptable: argument that if true allows the
### agent to disregard its direction

class Move(State):
	def parseArgs(self, args):
		self.squad = args[0]
		self.team = args[1]
		# self.interruptable = args[2]
		self.time = 0
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		# Look for enemies in attack range while moving
		if self.agent.isMoving():
			self.time += delta
			if self.time > 500:
				# Look for lowest hitpoint enemy, attack it first
				enemies = filter(lambda x, self=self: x.getTeam() != self.agent.getTeam() and distance(x.getLocation(), self.agent.getLocation()) <= BULLETRANGE, self.agent.getVisibleType(MOBAAgent))
				if enemies:
					self.agent.target = min(enemies, key=lambda x: x.getHitpoints())
					self.agent.changeState(Attack)
			return
		world = self.agent.world
		enemy_bases = world.getEnemyBases(self.team)
		my_base = world.getBaseForTeam(self.team)
		if distance(enemy_bases[0].getLocation(), self.agent.getLocation()) > BULLETRANGE:
			self.agent.navigateTo(enemy_bases[0].getLocation())
		# self.agent.changeState(Idle)
		# TODO: If you are offense, support low health allies or continue toward base
		# if self.squad == 'attacking':
		# 	pass
		# # TODO: If you are part of the backup, support medium health attackers or flank
		# elif self.squad == 'backup':
		# 	pass
		# # TODO: If you are defense, stay at the base and wait
		# elif self.squad == 'defense':
			# TODO: Get location of your base
			# If outside three times the length of the base's radius, move toward base
			# TODO: If outside of some radius, move toward it

##############################
### Pursue
###
### Follows the target enemy agent within attacking distance
###

class Pursue(State):
	def parseArgs(self, args):
		self.target = args[0]
	
	def execute(self, delta = 0):
		# TODO: Follow until enemy gets outside of "delta" of its goal (based on squad)
		pass

##############################
### Flank
###
### Find path with least amount of enemies
### 

class Flank(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		pass

##############################
### Support
###
### Group up with a struggling ally and attack its target
###

class Support(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		pass

##############################
### Defend
###
### Stay at the base and attack enemies who get within
### some distance of base

class Defend(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		pass

##############################
### Dodge
###
### While attacking, if a bullet is far enough away
### to be dodged then move out of its way.

class Dodge(State):
	def parseArgs(self, args):
		self.bullets = args[0]
	
	def execute(self, delta = 0):
		# TODO: Move in a direction perpendicular to bullet directions
		pass

##############################
### LockOn
###
### Finds a new target and begins to attack or pursue
### 

class LockOn(State):
	def parseArgs(self, args):
		self.enemies = args[0]
	
	def execute(self, delta = 0):
		# TODO: Find closest and weakest enemy
		# TODO: Alternatively attack Tower
		pass