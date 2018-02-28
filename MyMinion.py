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

# Allows for grouping of allies and coordinated attacks
squads = []

# Live friendly minion count
alive = 0

class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		self.target = None

		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)





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
		pass

##############################
### Move
###
### Move to the given position
### interruptable: argument that if true allows the
### agent to disregard its direction

class Move(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		pass

##############################
### Retreat
###
### Runs away from combat to a safer location
### 

class Retreat(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		pass

##############################
### Pursue
###
### Follows the target enemy agent within attacking distance
###

class Pursue(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
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

class Support(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		pass

##############################
### Dodge
###
### While attacking, if a bullet is far enough away
### to be dodged then move out of its way.

class Support(State):
	def parseArgs(self, args):
		pass
	
	def execute(self, delta = 0):
		pass