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
from itertools import combinations

# Creates the pathnetwork as a list of lines between all pathnodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent = None):
	lines = []
	### YOUR CODE GOES BELOW HERE ###
	# Get world lines
	w_lines = world.getLines()
	# Get a list of all possible point combinations
	p_lines = list(combinations(pathnodes, r=2))
	x_axis = (1,0)
	edg_a = None
	edg_b = None
	# Draw lines based on raycast from each pathnode to all other nodes
	for line in p_lines:
		# line = p_lines[6]
		# line = p_lines[1]
		dif_x = line[1][0] - line[0][0]
		dif_y = line[1][1] - line[0][1]
		# Get angle of line
		ang = angle(x_axis, (dif_x,dif_y))
		# Use angle of perpendicular to get offset for agent radius
		x_delt = agent.maxradius * math.sin(ang)
		y_delt = agent.maxradius * math.cos(ang)
		if dif_y >= 0:
			edg_a = ((line[0][0] + x_delt, line[0][1] - y_delt), (line[1][0] + x_delt, line[1][1] - y_delt))
			edg_b = ((line[0][0] - x_delt, line[0][1] + y_delt), (line[1][0] - x_delt, line[1][1] + y_delt))
		else:
			edg_a = ((line[0][0] + x_delt, line[0][1] + y_delt), (line[1][0] + x_delt, line[1][1] + y_delt))
			edg_b = ((line[0][0] - x_delt, line[0][1] - y_delt), (line[1][0] - x_delt, line[1][1] - y_delt))

		# Now check rayTrace for created lines
		if(not rayTraceWorld(line[0], line[1], w_lines) 
			and not rayTraceWorld(edg_a[0], edg_a[1], w_lines) 
			and not rayTraceWorld(edg_b[0], edg_b[1], w_lines)):
			# print math.degrees(ang)
			lines.append(line)
			# pygame.draw.line(world.debug, (255,0,0), edg_a[0], edg_a[1], 1)
			# pygame.draw.line(world.debug, (0,255,0), edg_b[0], edg_b[1], 1)
			
		# TODO: Check lines to see if agent size will cause collision during movement or at node
		# TODO: Find perpendicular line to given line, project a line by radius of agent and run rayTraceWorld on this
	### YOUR CODE GOES ABOVE HERE ###
	return lines
