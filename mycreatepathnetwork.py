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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *
from itertools import permutations

def collidedWithNonParallel(p1, p2, lines):
	coll = rayTraceWorldNoEndPoints(p1, p2, lines)
	if coll:
		coll = (round(coll[0]), round(coll[1]))
	if coll == p1 or coll == p2:
		return False
	return coll

def noPointsInPolygon(poly, w_points):
	for point in w_points:
		if pointInsidePolygonPoints(point, poly):
			return False
	return True

def appendPolyNoDuplicates(poly, poly_list):
	for permut in permutations(poly):
		if poly_list.count(permut):
			return
	poly_list.append(poly)
	
# Creates a pathnode network that connects the midpoints of each navmesh together
def myCreatePathNetwork(world, agent = None):
	nodes = []
	edges = []
	polys = []
	### YOUR CODE GOES BELOW HERE ###

	w_points = world.getPoints()
	obj_points = w_points[4:]
	w_lines = world.getLines()

	# TODO: For every point, try to make a triangle with every other point in scene
	for a in w_points:
		for b in filter(lambda x, a=a: x != a, w_points):
			if not collidedWithNonParallel(a, b, w_lines):
				for c in filter(lambda x, a=a, b=b: x != a and x != b, w_points):
					if not collidedWithNonParallel(b, c, w_lines) \
						and not collidedWithNonParallel(a, c, w_lines) \
						and noPointsInPolygon((a,b,c), \
						filter(lambda x, a=a, b=b, c=c: x != a and x != b and x != c, w_points)):
						# Valid triangle! Yay
						appendPolyNoDuplicates((a,b,c), polys)
						appendLineNoDuplicates((a,b), w_lines)
						appendLineNoDuplicates((a,c), w_lines)
						appendLineNoDuplicates((c,b), w_lines)
						# pygame.draw.polygon(world.debug, (0, 255, 0), (a, b, c), 2)

	# TODO: Ensure triangles do not get made inside objects
	for tri in list(polys):
		for obj in world.getObstacles():
			tmpobj = set(obj.getPoints())
			if tmpobj.issuperset(list(tri)):
				polys.remove(tri)

	for tri in polys:
		pygame.draw.polygon(world.debug, (255, 0, 0), tri, 2)

	### YOUR CODE GOES ABOVE HERE ###
	return nodes, edges, polys

	
