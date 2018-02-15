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

from math import sin, cos

from constants import *
from utils import distance
from core import *
from mycreatepathnetwork import myCreatePathNetwork
from mynavigatorhelpers import *
import heapq

###############################
### Priority Queue
###
### Uses the heapq library to create a priority queue
class PriorityQueue(object):
    """
    A queue structure where each element is served in order of priority.

    Elements in the queue are popped based on the priority with higher priority
    elements being served before lower priority elements.  If two elements have
    the same priority, they will be served in the order they were added to the
    queue.

    Attributes:
        queue (list): Nodes added to the priority queue.
        current (int): The index of the current node in the queue.
    """

    def __init__(self):
        """Initialize a new Priority Queue."""
        self.queue = []
        self.nodes = {}
        self.unique_id = 0

    def pop(self):
        """
        Pop top priority node from queue.

        Returns:
            The node with the highest priority.
        """

        while self.queue:
            priority, unique_id, node_id = heapq.heappop(self.queue)
            if node_id is not None:
                del self.nodes[unique_id]
                return (priority, node_id)
        raise BaseException('The queue is empty')

    def remove(self, node_id):
        """
        Remove a node from the queue.

        This is a hint, you might require this in ucs,
        however, if you choose not to use it, you are free to
        define your own method and not use it.

        Args:
            node_id (int): Index of node in queue.
        """
        # Retrieve node object from nodes list
        node = self.nodes.pop(node_id)
        # Update node id to reflect None (or Removed)
        node[-1] = None


    def __iter__(self):
        """Queue iterator."""

        return iter(sorted(self.queue))

    def __str__(self):
        """Priority Queue to string."""

        return 'PQ:%s' % self.queue

    def append(self, node):
        """
        Append a node to the queue.

        Args:
            node: Comparable Object to be added to the priority queue.
        """

        # Increment the unique id counter
        self.unique_id += 1
        # create node entry with layout of priority, unique id, node id
        node_entry = [node[0], self.unique_id, node[-1]]
        # add node entry to the list of nodes, indexed by its node id
        self.nodes[self.unique_id] = node_entry
        # finally push node_entry onto heap
        heapq.heappush(self.queue, node_entry)

    def __contains__(self, key):
        """
        Containment Check operator for 'in'
        """

        return key in [n for _, n in self.queue]

    def __eq__(self, other):
        """
        Compare this Priority Queue with another Priority Queue.
        """

        return self == other

    def size(self):
        """
        Get the current size of the queue.
        """

        return len(self.queue)

    def clear(self):
        """Reset queue to empty (no nodes)."""
        self.queue = []

    def top(self):
        """
        Get the top item in the queue.
        """

        return self.queue[0]



###############################
### AStarNavigator
###
### Creates a path node network and implements the A* algorithm to create a path to the given destination.
            
class AStarNavigator(NavMeshNavigator):

    def __init__(self):
        NavMeshNavigator.__init__(self)
        

    ### Create the path node network.
    ### self: the navigator object
    ### world: the world object
    def createPathNetwork(self, world):
        self.pathnodes, self.pathnetwork, self.navmesh = myCreatePathNetwork(world, self.agent)
        return None
        
    ### Finds the shortest path from the source to the destination using A*.
    ### self: the navigator object
    ### source: the place the agent is starting from (i.e., its current location)
    ### dest: the place the agent is told to go to
    def computePath(self, source, dest):
        self.setPath(None)
        ### Make sure the next and dist matrices exist
        if self.agent != None and self.world != None: 
            self.source = source
            self.destination = dest
            ### Step 1: If the agent has a clear path from the source to dest, then go straight there.
            ###   Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
            ###   Tell the agent to move to dest
            ### Step 2: If there is an obstacle, create the path that will move around the obstacles.
            ###   Find the path nodes closest to source and destination.
            ###   Create the path by traversing the self.next matrix until the path node closest to the destination is reached
            ###   Store the path by calling self.setPath()
            ###   Tell the agent to move to the first node in the path (and pop the first node off the path)
            if clearShot(source, dest, self.world.getLines(), self.world.getPoints(), self.agent):
                self.agent.moveToTarget(dest)
            else:
                start = findClosestUnobstructed(source, self.pathnodes, self.world.getLinesWithoutBorders())
                end = findClosestUnobstructed(dest, self.pathnodes, self.world.getLinesWithoutBorders())
                if start != None and end != None:
                    # print len(self.pathnetwork)
                    newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates())
                    # print len(newnetwork)
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

    ### This function gets called by the agent to figure out if some shortcuts can be taken when traversing the path.
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


def get_children(parent, network):
    children = []
    for line in network:
        if line[0] == parent:
            children.append(line[1])
        elif line[1] == parent:
            children.append(line[0])
    return children

def astar(init, goal, network):
    path = []
    closed = set() # Another name for explored
    ### YOUR CODE GOES BELOW HERE ###
    frontier = PriorityQueue()
    node_data = {}
    # Initialize frontier and node_data map with start state
    frontier.append((0, init))
    node_data[init] = (None, 0)
    while True:
        exploring = frontier.pop()
        if exploring[-1] == goal:
            state = exploring[-1]
            parent = node_data[state][0]
            while parent:
                path.append(state)
                state = parent
                parent = node_data[state][0]
            path.append(state)
            list.reverse(path)
            return path, closed
        elif exploring[-1] in closed:
            continue
        parent = exploring[-1]
        children = get_children(parent, network)
        closed.add(exploring[1])
        parent_cost = node_data[parent][1]
        for state in children:
            g = distance(parent, state) + parent_cost
            h = distance(state, goal)
            cost = g + h
            if state not in node_data or node_data[state][1] > g:
                node_data[state] = (parent, g)
            if state not in closed:
                frontier.append((cost, state))

    ### YOUR CODE GOES ABOVE HERE ###
    return path, closed
    
    


def myUpdate(nav, delta):
    ### YOUR CODE GOES BELOW HERE ###

    ### YOUR CODE GOES ABOVE HERE ###
    return None



def myCheckpoint(nav):
    ### YOUR CODE GOES BELOW HERE ###

    ### YOUR CODE GOES ABOVE HERE ###
    return None


### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
    ### YOUR CODE GOES BELOW HERE ###

    line = (p1, p2)
    x_axis = (1, 0)
    edg_a = None
    edg_b = None

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
    return not rayTraceWorldNoEndPoints(line[0], line[1], worldLines) \
    and not rayTraceWorldNoEndPoints(edg_a[0], edg_a[1], worldLines) \
    and not rayTraceWorldNoEndPoints(edg_b[0], edg_b[1], worldLines) \
    and not rayTraceWorldNoEndPoints(edg_a[0], edg_b[1], worldLines)

    ### YOUR CODE GOES ABOVE HERE ###
    return False

