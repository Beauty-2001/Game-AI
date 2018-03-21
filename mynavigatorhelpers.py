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

import sys, pygame, random, time, copy
from pygame.locals import *

import numpy as np
from math import sin, cos
from constants import *
from utils import *
from core import *

def rayTraceAgentDependent(p1, p2, worldLines, agent):
    if p1 == p2:
        return False
    line = (p1, p2)
    x_axis = (1, 0)
    edg_a = None
    edg_b = None

    dif_x = line[1][0] - line[0][0]
    dif_y = line[1][1] - line[0][1]
    # Get angle of line
    # print (dif_x, dif_y)
    ang = angle(x_axis, (dif_x, dif_y))
    # Use angle of perpendicular to get offset for agent radius
    x_delt = (agent.maxradius) * sin(ang)
    y_delt = (agent.maxradius) * cos(ang)
    if dif_y >= 0:
        edg_a = ((line[0][0] + x_delt, line[0][1] - y_delt),
                (line[1][0] + x_delt, line[1][1] - y_delt))
        edg_b = ((line[0][0] - x_delt, line[0][1] + y_delt),
                (line[1][0] - x_delt, line[1][1] + y_delt))
    else:
        edg_a = ((line[0][0] + x_delt, line[0][1] + y_delt),
                (line[1][0] + x_delt, line[1][1] + y_delt))
        edg_b = ((line[0][0] - x_delt, line[0][1] - y_delt),
                (line[1][0] - x_delt, line[1][1] - y_delt))

    # Now check rayTrace for created lines
    # Check lines to see if agent size will cause collision during movement or at node
    return not rayTraceWorldNoEndPoints(line[0], line[1], worldLines) \
    and not rayTraceWorldNoEndPoints(edg_a[0], edg_a[1], worldLines) \
    and not rayTraceWorldNoEndPoints(edg_b[0], edg_b[1], worldLines) \
    and not rayTraceWorldNoEndPoints(edg_a[0], edg_b[1], worldLines)

### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
    ### YOUR CODE GOES BELOW HERE ###
    # TODO: Collapse where available
    w_lines = world.getLinesWithoutBorders()
    path.insert(0,source)
    path.append(dest)
    newpath = []
    point = source
    while point != dest:
        if not point:
            return path
        idx = path.index(point)
        newpath.append(findFurthestUnobstructedOnPath(point, path[idx:], w_lines, agent))
        point = newpath[-1]

    path = newpath
    # path.insert(0, source)
    # path.append(dest)
    # newPath = [path[0]]
    # end = len(path) - 1
    # i = 0
    # for _ in xrange(0, end):
    #     i+=1
    #     for j in xrange(end, i, -1):
    #         if rayTraceAgentDependent(path[i], path[j], world.getLinesWithoutBorders(), agent):
    #             newPath.append(path[j])
    #             i = j - 1
    #             break

    # path = newPath

    # knots = [
    #     0, 0, 0, 1, 2, 2, 2
    # ]
    # path = []
    # degree = 2
    # # Interpolation just for fun
    # for t in np.arange(0, 1, 0.01):
    #     path.append(interpolation(t, newPath, degree, knots))

    ### YOUR CODE GOES BELOW HERE ###
    return path


### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
    ### YOUR CODE GOES BELOW HERE ###

    ### YOUR CODE GOES ABOVE HERE ###
    return False

def interpolation(t, points, degree = 1, knots = None, weights = None):
    n = len(points)
    dim = len(points[0])

    if not weights:
        weights = np.full(n, 1)
    if not knots or len(knots) > n+degree+1:
        knots = np.arange(0, n+degree+1)

    domain = [degree, len(knots)-degree-1]

    # Make t fit the domain of the spline
    low = knots[domain[0]]
    high = knots[domain[1]]
    t = t * (high - low) + low

    # t should be between low and high

    # find s for t
    for s in xrange(domain[0], domain[1]):
        if t >= knots[s] and t <= knots[s+1]:
            break

    # Convert to homogenious coords
    v = []
    for i in xrange(0, n):
        v.append([])
        for j in xrange(0, dim):
            v[i].append(points[i][j] * weights[i])
        v[i].append(weights[i])

    # level goes form 1 to curve degree
    for l in xrange(1, degree + 2):
        for i in xrange(s, s-degree-1+l, -1):
            alpha = (t - knots[i]) / (knots[i+degree+1-l] - knots[i])

            for j in xrange(0, dim):
                v[i][j] = (1 - alpha) * v[i-1][j] + alpha * v[i][j]

    result = []
    for i in xrange(0, dim):
        result.append(v[s][i] / v[s][dim])

    return result


# Find the point in nodes closest to p that is unobstructed
# NOTE: This implementation fixes the problem of clearance
def findClosestUnobstructed_fix(p, nodes, worldLines, agent):
    best = None
    dist = INFINITY
    for n in nodes:
        if rayTraceAgentDependent(p, n, worldLines, agent):
            d = distance(p, n)
            if best == None or d < dist:
                best = n
                dist = d
    return best

def findFurthestUnobstructedOnPath(p, path, worldLines, agent):
    best = None
    dist = -INFINITY
    for n in path:
        if rayTraceAgentDependent(p, n, worldLines, agent):
            d = distance(p, n)
            if best == None or d > dist:
                best = n
                dist = d
    return best