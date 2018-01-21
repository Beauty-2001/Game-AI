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
	# Draw lines based on raycast from each pathnode to all other nodes
	for line in p_lines:
		if(not rayTraceWorld(line[0], line[1], w_lines)):
			lines.append(line)
		# TODO: Check lines to see if agent size will cause collision during movement or at node
		# TODO: Find perpendicular line to given line, project a line by radius of agent and run rayTraceWorld on this
	### YOUR CODE GOES ABOVE HERE ###
	return lines
