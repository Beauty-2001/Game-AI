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

from utils import rayTraceWorldNoEndPoints, pointInsidePolygonPoints, polygonsAdjacent, isConvex, appendLineNoDuplicates, angle, drawCross, reverseLine
from itertools import permutations, combinations
from math import sin, cos

def lineInSet(p0, p1, lines):
    return lines.count((p0, p1)) or lines.count((p1,p0))

def collidedWithNonParallel(p1, p2, lines):
    coll = rayTraceWorldNoEndPoints(p1, p2, lines)
    if coll:
        coll = (math.ceil(coll[0]), math.ceil(coll[1]))
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

def removeLineDuplicates(line, line_list):
    line_list.remove(line)
    line_list.remove(reverseLine(line))

origin = (0,0)
refvec = [0,1]

def clockwiseangle_and_distance(point):
    # Vector between point and origin v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod = normalized[0]*refvec[0] + normalized[1]*refvec[1]		# x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]	# x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle
    # Return first angle as its primary sorting criteria, if two vectors have same angle
    # shorter distance should come first
    return angle

# Used to recursively expand a polygon given the other polygons in the scene
def expandPoly(poly, o_polys):
    global origin
    for obj in filter(lambda x, poly=poly: x != poly, o_polys):
        if polygonsAdjacent(poly, obj):
            shape = list(set(poly + obj))
            origin = shape[-1]
            shape = tuple(sorted(shape, key=clockwiseangle_and_distance))
            if isConvex(shape):
                o_polys.remove(poly)
                o_polys.remove(obj)
                appendPolyNoDuplicates(shape, o_polys)
                return expandPoly(shape, o_polys)
    return

# Creates a pathnode network that connects the midpoints of each navmesh together
def myCreatePathNetwork(world, agent = None):
    nodes = set()
    edges = []
    polys = []
    ### YOUR CODE GOES BELOW HERE ###
    w_lines = world.getLines()
    w_points = sorted(world.getPoints(), key=clockwiseangle_and_distance)

    # For every point, try to make a triangle with every other point in scene
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
                        appendLineNoDuplicates((b,c), w_lines)

    # Ensure triangles do not get made inside objects
    for tri in list(polys):
        for obj in world.getObstacles():
            tmpobj = set(obj.getPoints())
            if tmpobj.issuperset(list(tri)):
                polys.remove(tri)

    poly_len = 0
    # Merge triangles into convex polys
    while poly_len != len(polys):
        poly_len = len(polys)
        for tri in polys:
            expandPoly(tri, polys)

    x_axis = (1, 0)
    edg_a = None
    edg_b = None

    # Create nodes and edges using center, mid-point of lines, and corners of polygon
    for poly in polys:
        w_lines = world.getLines()
        l_lines = []
        # Center
        l_nodes = set()
        # Midpoint of lines
        for i in xrange(-1, len(poly)-1):
            if not lineInSet(poly[i], poly[i+1], w_lines):
                node_a = ((3 * poly[i][0] + poly[i+1][0]) / 4, 
                          (3 * poly[i][1] + poly[i+1][1]) / 4)
                l_nodes.add(node_a)
                node_b = ((poly[i][0] + 3 * poly[i+1][0]) / 4, 
                          (poly[i][1] + 3 * poly[i+1][1]) / 4)
                l_nodes.add(node_b)
                node_c = ((poly[i][0] + poly[i+1][0]) / 2,
                          (poly[i][1] + poly[i+1][1]) / 2)
                l_nodes.add(node_c)
                l_lines += list(permutations([node_a, node_b, node_c], 2))

        # Get edges
        p_lines = set(combinations(l_nodes, 2)).difference(l_lines)
        for line in p_lines:
            dif_x = line[1][0] - line[0][0]
            dif_y = line[1][1] - line[0][1]
            # Get angle of line
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
            if not rayTraceWorldNoEndPoints(line[0], line[1], w_lines) \
            and not rayTraceWorldNoEndPoints(edg_a[0], edg_a[1], w_lines) \
            and not rayTraceWorldNoEndPoints(edg_b[0], edg_b[1], w_lines) \
            and not rayTraceWorldNoEndPoints(edg_a[0], edg_b[1], w_lines) \
            and not rayTraceWorldNoEndPoints(line[0], line[1], edges):
                appendLineNoDuplicates(line, edges)
                nodes.add(line[0])
                nodes.add(line[1])
                drawCross(world.debug, line[0])
                drawCross(world.debug, line[1])
            else:
                drawCross(world.debug, line[0], (255,0,0))
                drawCross(world.debug, line[1], (255,0,0))

    ### YOUR CODE GOES ABOVE HERE ###
    return nodes, edges, polys