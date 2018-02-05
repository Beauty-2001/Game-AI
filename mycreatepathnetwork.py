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

# Creates a pathnode network that connects the midpoints of each navmesh together
def myCreatePathNetwork(world, agent = None):
	nodes = []
	edges = []
	polys = []
	### YOUR CODE GOES BELOW HERE ###

	# Draw edges from every corner of the world to unobstructed points
	w_points = world.getPoints()
	w_lines = world.getLinesWithoutBorders()
	edge_points = w_points[:4]
	obj_points = w_points[4:]
	for edge in edge_points:
		for obj in obj_points:
			if (not rayTraceWorldNoEndPoints(obj, edge, w_lines)):
				edges.append((edge, obj))
				# Also check if edges are overlapping from previous
				w_lines.append((edge, obj))
				pygame.draw.line(world.debug, (0,0,255), edge, obj, 1)
	# Cleanup
	del edge_points
	# TODO: Draw lines from all object points to other unobstructed object points
	objs = world.getObstacles()
	pnt_set = set(obj_points)
	for obj in objs:
		# Remove inter-object points from consideration
		reduced = list(pnt_set.difference(obj.points))
		for point in obj.getPoints():
			for dest in reduced:
				if (not rayTraceWorldNoEndPoints(point, dest, w_lines)):
					edges.append((point, dest))
					w_lines.append((point, dest))
					pygame.draw.line(world.debug, (255, 0, 0), point, dest, 1)

	# TODO: Also check if intersect with previously drawn edges

	### YOUR CODE GOES ABOVE HERE ###
	return nodes, edges, polys

	
