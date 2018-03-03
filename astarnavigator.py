import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *
from mycreatepathnetwork import *
from mynavigatorhelpers import *


###############################
### AStarNavigator
###
### Creates a path node network and implements the FloydWarshall all-pairs shortest-path algorithm to create a path to the given destination.

class AStarNavigator(NavMeshNavigator):

	def __init__(self):
		NavMeshNavigator.__init__(self)


	### Create the pathnode network and pre-compute all shortest paths along the network.
	### self: the navigator object
	### world: the world object
	def createPathNetwork(self, world):
		self.pathnodes, self.pathnetwork, self.navmesh = myCreatePathNetwork(world, self.agent)
		return None

	### Finds the shortest path from the source to the destination using A*.
	### self: the navigator object
	### source: the place the agent is starting from (i.e., it's current location)
	### dest: the place the agent is told to go to
	def computePath(self, source, dest):
		### Make sure the next and dist matricies exist
		if self.agent != None and self.world != None:
			self.source = source
			self.destination = dest
			### Step 1: If the agent has a clear path from the source to dest, then go straight there.
			###   Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
			###   Tell the agent to move to dest
			### Step 2: If there is an obstacle, create the path that will move around the obstacles.
			###   Find the pathnodes closest to source and destination.
			###   Create the path by traversing the self.next matrix until the pathnode closes to the destination is reached
			###   Store the path by calling self.setPath()
			###   Tell the agent to move to the first node in the path (and pop the first node off the path)
			if clearShot(source, dest, self.world.getLinesWithoutBorders(), self.world.getPoints(), self.agent):
				self.agent.moveToTarget(dest)
			else:
				start = findClosestUnobstructed(source, self.pathnodes, self.world.getLinesWithoutBorders())
				end = findClosestUnobstructed(dest, self.pathnodes, self.world.getLinesWithoutBorders())
				if start != None and end != None:
					#print len(self.pathnetwork)
					newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates())
					#print len(newnetwork)
					#print "ok"
					closedlist = []
					path, closedlist = astar(start, end, newnetwork)
					if path is not None and len(path) > 0:
						path = shortcutPath(source, dest, path, self.world, self.agent)
						self.setPath(path)
						if self.path is not None and len(self.path) > 0:
							first = self.path.pop(0)
							self.agent.moveToTarget(first)
		return None

	### Called when the agent gets to a node in the path.
	### self: the navigator object
	def checkpoint(self):
		myCheckpoint(self)
		return None

	### This function gets called by the agent to figure out if some shortcutes can be taken when traversing the path.
	### This function should update the path and return True if the path was updated.
	def smooth(self):
		return mySmooth(self)

	def update(self, delta):
		myUpdate(self, delta)


def unobstructedNetwork(network, worldLines):
	newnetwork = []
	for l in network:
		hit = rayTraceWorld(l[0], l[1], worldLines)
		if hit == None:
			newnetwork.append(l)
	return newnetwork


def foom (OO0OOO000OO0O000O ,O0O000OOOOOOO0O0O ,func =lambda O0OO0OOO00000OO0O :O0OO0OOO00000OO0O ):#line:1
	for OO00O0OOO0O0O0OO0 in xrange (len (O0O000OOOOOOO0O0O )):#line:2
		if func (OO0OOO000OO0O000O )<func (O0O000OOOOOOO0O0O [OO00O0OOO0O0O0OO0 ]):#line:3
			O0O000OOOOOOO0O0O .insert (OO00O0OOO0O0O0OO0 ,OO0OOO000OO0O000O )#line:4
			return O0O000OOOOOOO0O0O #line:5
	O0O000OOOOOOO0O0O .append (OO0OOO000OO0O000O )#line:6
	return O0O000OOOOOOO0O0O #line:7
def astar (O0O00O000OO0O0OO0 ,O0OO0OOOOOO0OO0OO ,O00000O0OOO0OOOO0 ):#line:10
	O0OOO0OOOOO0O00OO =[]#line:11
	O0000OO00O0OOO0OO =[]#line:12
	OOO0O0O0OO0OOO00O =[]#line:13
	O0O00O000OO0O0OO0 =(O0O00O000OO0O0OO0 ,0 ,distance (O0O00O000OO0O0OO0 ,O0OO0OOOOOO0OO0OO ),None )#line:16
	OOO0O0O0OO0OOO00O =set ()#line:17
	OO00O0000OO000O00 =set ()#line:18
	O0000OO00O0OOO0OO =[O0O00O000OO0O0OO0 ]#line:19
	O00OO0OOOO00000OO =O0O00O000OO0O0OO0 #line:20
	while O00OO0OOOO00000OO is not None and O00OO0OOOO00000OO [0 ]!=O0OO0OOOOOO0OO0OO and len (O0000OO00O0OOO0OO )>0 :#line:23
		OOO0O0O0OO0OOO00O .add (O00OO0OOOO00000OO [0 ])#line:24
		OO00O0000OO000O00 .add (O00OO0OOOO00000OO )#line:25
		O0000OO00O0OOO0OO .pop (0 )#line:26
		O0O00O0000OOO0OOO =fooz (O00OO0OOOO00000OO ,O00000O0OOO0OOOO0 ,O0OO0OOOOOO0OO0OO )#line:28
		for OO000O00O0000O0OO in O0O00O0000OOO0OOO :#line:30
			if OO000O00O0000O0OO [0 ]not in OOO0O0O0OO0OOO00O :#line:31
				foom (OO000O00O0000O0OO ,O0000OO00O0OOO0OO ,lambda O0OO0O0O000OO00O0 :O0OO0O0O000OO00O0 [1 ]+O0OO0O0O000OO00O0 [2 ])#line:32
		if len (O0000OO00O0OOO0OO )>0 :#line:34
			O00OO0OOOO00000OO =O0000OO00O0OOO0OO [0 ]#line:35
		else :#line:36
			O00OO0OOOO00000OO =None #line:37
	if O00OO0OOOO00000OO is not None :#line:40
		while O00OO0OOOO00000OO [3 ]is not None :#line:41
			O0OOO0OOOOO0O00OO .append (O00OO0OOOO00000OO [0 ])#line:42
			O00O0O000O000OOO0 =O00OO0OOOO00000OO [3 ]#line:43
			for OO00O0O000O000O0O in list (OO00O0000OO000O00 ):#line:44
				if O00O0O000O000OOO0 ==OO00O0O000O000O0O [0 ]:#line:45
					O00OO0OOOO00000OO =OO00O0O000O000O0O #line:46
					break #line:47
		O0OOO0OOOOO0O00OO .append (O00OO0OOOO00000OO [0 ])#line:48
		O0OOO0OOOOO0O00OO .reverse ()#line:49
	OOO0O0O0OO0OOO00O =list (OOO0O0O0OO0OOO00O )#line:50
	return O0OOO0OOOOO0O00OO ,OOO0O0O0OO0OOO00O #line:52
def fooz (OO0OOOOOOO00O0O0O ,OOOOOO0OOOOOOO000 ,OO00O0O000O0OOO0O ):#line:55
	OO0OOOO0O0O0OOOOO =[]#line:56
	for OO0O00O0OO00OOO00 in OOOOOO0OOOOOOO000 :#line:57
		if OO0O00O0OO00OOO00 [0 ]==OO0OOOOOOO00O0O0O [0 ]:#line:58
			OO0OOOO0O0O0OOOOO .append ((OO0O00O0OO00OOO00 [1 ],OO0OOOOOOO00O0O0O [1 ]+distance (OO0O00O0OO00OOO00 [0 ],OO0O00O0OO00OOO00 [1 ]),distance (OO0O00O0OO00OOO00 [1 ],OO00O0O000O0OOO0O ),OO0OOOOOOO00O0O0O [0 ]))#line:59
		elif OO0O00O0OO00OOO00 [1 ]==OO0OOOOOOO00O0O0O [0 ]:#line:60
			OO0OOOO0O0O0OOOOO .append ((OO0O00O0OO00OOO00 [0 ],OO0OOOOOOO00O0O0O [1 ]+distance (OO0O00O0OO00OOO00 [0 ],OO0O00O0OO00OOO00 [1 ]),distance (OO0O00O0OO00OOO00 [0 ],OO00O0O000O0OOO0O ),OO0OOOOOOO00O0O0O [0 ]))#line:61
	return OO0OOOO0O0O0OOOOO #line:62
def myUpdate (OO0OOO00O0OO00O00 ,O0OOO0000OOOO00OO ):#line:66
	if OO0OOO00O0OO00O00 .getPath ()is not None :#line:68
		OOOO000O0OOO00000 =OO0OOO00O0OO00O00 .world .getGates ()#line:69
		OO0O000O000O0000O =OO0OOO00O0OO00O00 .agent .getLocation ()#line:79
		for OO0O00OOO0000OOOO in OO0OOO00O0OO00O00 .getPath ()+[OO0OOO00O0OO00O00 .getDestination ()]:#line:80
			if OO0O000O000O0000O is not None :#line:81
				O00O0OO0O000000O0 =rayTraceWorld (OO0O000O000O0000O ,OO0O00OOO0000OOOO ,OOOO000O0OOO00000 )#line:82
				if O00O0OO0O000000O0 is not None :#line:83
					OO0OOO00O0OO00O00 .setPath (None )#line:85
					OO0OOO00O0OO00O00 .agent .stopMoving ()#line:86
					return None #line:87
			OO0O000O000O0000O =OO0O00OOO0000OOOO
		return None #line:108
def myCheckpoint (O0OOOOOOO0OOOO000 ):#line:113
	""#line:128
	return None #line:130
def clearShot (OO0O0OO0000O00OOO ,O00O00O0OOO0OO00O ,O00O0O0OOO0OO0OOO ,O0OO00OO0O0OOO000 ,OOO00OOOOOO00OOOO ):#line:139
	O0O00OO000O0O00OO =OOO00OOOOOO00OOOO .getRadius ()*4.0 #line:141
	OOOO00OOO0O00OO00 =rayTraceWorld (OO0O0OO0000O00OOO ,O00O00O0OOO0OO00O ,O00O0O0OOO0OO0OOO )#line:142
	if OOOO00OOO0O00OO00 ==None :#line:143
		O00O0000O00OO0000 =False #line:144
		for OOOO00000O0O0OO0O in O0OO00OO0O0OOO000 :#line:145
			if minimumDistance ((OO0O0OO0000O00OOO ,O00O00O0OOO0OO00O ),OOOO00000O0O0OO0O )<O0O00OO000O0O00OO :#line:146
				O00O0000O00OO0000 =True #line:147
		if not O00O0000O00OO0000 :#line:148
			return True #line:149
	return False
#e9015584e6a44b14988f13e2298bcbf9


#===============================================================#
# Obfuscated by Oxyry Python Obfuscator (http://pyob.oxyry.com) #
#===============================================================#
