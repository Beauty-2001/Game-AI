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

# Creates a grid as a 2D array of True/False values (True = traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
    grid = None
    dimensions = (0, 0)
    ### YOUR CODE GOES BELOW HERE ###
    # Get dims
    world_dims = world.getDimensions()
    # Get obstacle lines omitting world boundaries
    lines = world.getLinesWithoutBorders()
    # Calculate number of cells
    gridcols = int(world_dims[0]/cellsize)
    gridrows = int(world_dims[1]/cellsize)
    dimensions = (gridcols, gridrows)
    # Create MxN grid initialized to True
    grid = numpy.full((gridcols, gridrows), True)
    # TODO: Initial check to see if inside object
    for col in xrange(gridcols):
        for row in xrange(gridrows):
            x = col * cellsize
            y = row * cellsize
            uleft = (x, y)
            lleft = (x, y + cellsize)
            uright = (x + cellsize, y)
            lright = (x + cellsize, y + cellsize)
            is_inside = pointInsidePolygonLines(uleft, lines)
            if(not is_inside):
                left = rayTraceWorld(uleft, lleft, lines)
                right = rayTraceWorld(uright, lright, lines)
                top = rayTraceWorld(uleft, uright, lines)
                bottom = rayTraceWorld(lleft, lright, lines)
                is_inside = left or right or top or bottom
            grid[col][row] = not is_inside

    # TODO: Find lines of grid box
    # TODO: Check if those lines intersect with any object

    ### YOUR CODE GOES ABOVE HERE ###
    return grid, dimensions
