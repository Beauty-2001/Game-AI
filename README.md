# GameAI-Assignments

# Homework 1: Grid Navigation

The purpose of this exercise is to acquaint you with the Python game
engine we will be using in the class.

One of the main uses of artificial intelligence in games is to perform
*path planning*, the search for a sequence of movements through the
virtual environment that gets an agent from one location to another
without running into any obstacles. For now, we will assume static
obstacles. In order for an agent to engage in path planning, there must
be a topography for the agent to traverse that is represented in a form
that can be efficiently reasoned about. The simplest topography is a
grid. Think of an imaginary lattice of cells superimposed over an
environment such that an agent can be in one cell at a time. Moving in a
grid is relatively straightforward: from any cell, an agent can traverse
to any of its four (or eight) neighboring cells.

[![](instructions/grid.png)](grid.png)

In this assignment, you will write the code to superimpose a grid over
any given terrain so that an agent can navigate by moving left, right,
up, or down from cell to cell. The code to generate the grid should work
on any terrain such that an agent can never collide with an obstacle.

But first, you need to become familiar with the python game engine in
which you will be working.

-----

## What you need to know

The game engine is object-oriented. The primary object is the
**GameWorld**, which is a container for all other obstacles. Most
importantly, the GameWorld object contains the terrain of the virtual
environment. The terrain is represented as a list of **Obstacle**
objects, which themselves are polygons—lists of points such that there
is a line between every adjacent point (and the first and last points in
the list. The GameWorld also manages the agents, bullets, resources
(things that agents can gather) and computes collisions between all
objects and obstacles. The GameWorld also does important stuff like run
the real-time game loop and maintain the rendering windows, but you
shouldn't need to worry about that. What you do need to know is that
every iteration of the game loop, called a *tick*, the update method is
called on all dynamic objects.

Below are the important bits of information about objects that you will
be working with or need to know about for this assignment.

### GameWorld

GameWorld is defined in core.py

Member functions:

getPoints(): returns a list of all the corners of all obstacles (and the
edges of the screen). A point is a tuple of the form (x, y).

getLines(): returns a list of all lines in the polygon. A line is a
tuple of the form (point1, point2) where points are tuples of the form
(x, y).

pointInside(point): returns True if a point (x, y) is inside the
obstacle.

### Agent

Agent is defined in core.py. Agent is the class type of the player
avatar or non-player characters. Aside from drawing itself, an Agent
knows how to move (which it inherits from its super-class Mover) and
shoot. If it is moving to a particular destination, it updates its
location every tick. Agents maintain a timer to control how often it can
shoot.

While the Agent class does know how to move in a straight line toward a
given point, it does not know how to move around an environment *without
colliding with obstacles*. When instructed to move, it will move in a
straight line from its current position to a target position. The
intelligence in how to avoid obstacles is contained in a sub-component
of the Agent, called the **Navigator**.

Member variables:

  - moveTarget: the (x, y) point to which the agent has been instructed
    to move to. Used for interpolating the Agent's current position at
    any given tick.
  - navigator: an object that tells the agent how to move.

Member functions:

  - moveToTarget(point): Instructs the Agent to move straight to the
    point (x, y), ignoring the existence of obstacles.
  - navigateTo(point): Instructs the Agent to create a path through the
    environment that avoids collisions. This function invokes the
    navigator's computePath() functionality.
  - isMoving(): returns True if the agent is currently moving.
  - getMoveTarget(): returns the point that the agent is currently
    moving toward.
  - stopMoving(): stops the Agent from moving

### Navigator

Navigator is defined in core.py. A Navigator contains the smarts for how
to get around in the game world without running into obstacles. Think of
it as a brain that gets attached to an agent that controls its movement.
Its primary function is to compute a path between two points that steers
the Agent clear of any obstacles. A path is a set of intermediate
way-points that the agent should navigate to in pursuit of arriving
safely at its ultimate destination. Path planning can be done in many
different ways and different AI techniques will sub-class from
Navigator. Once a path is computed, it sends call-back messages to the
Agent to move from intermediate way-point to intermediate way-point.

Member variables:

agent: pointer back to the Agent object that is being guided by the AI.

world: pointer to the GameWorld object

source: the point (x, y) from which navigation started.

destination: the point (x, y) to which the Agent must traverse.

path: a list of points to traverse in order that is guaranteed not to
result in a collision with an obstacle.

Member functions:

  - computePath(source, destination): Find a path through the terrain
    (causing path to be not None) and call back to the Agent to start
    moving. This default functionality just instructs the agent to move
    straight to the destination. This function will be overridden by
    sub-classes implementing particular path planning techniques.
  - doneMoving(): the Navigator invokes this function when the agent has
    reached its moveTarget. doneMoving contains logic to determine what
    to do next. If there is a path, it will select the next point in the
    path as the next moveTarget and call back to the Agent.
  - checkpoint(): called when the Agent reaches a point on the path.
  - smooth(): optimizes the path to take shortcuts whenever possible and
    thereby create smoother, more efficient motion.

### GridNavigator

GridNavigator is defined in gridnavigator.py. GridNavigator specializes
the Navigator "brain" to work on grid topologies.

Member variables:

  - grid: A two-dimensional array of booleans such that
    grid\[column\]\[row\] indicates whether the cell can be entered by
    an agent.
  - dimensions: A tuple (columns, rows) indicating the number of columns
    and rows in the grid.
  - cellSize: A scalar value indicating the height and width of a cell.
    It is based on the size of the agent.

Member functions:

  - createGrid(world): Function creates the grid by looking at the
    obstacles in the world and marking cells in the grid as True if
    traversable or False if non-traversable. This function sets the grid
    member variable and the dimensions member variable. To do this,
    createGrid() calls myCreateGrid(world, agent), a non-member function
    that returns two values: the 2D array of the grid and the dimensions
    in the form (columns, rows).

### GreedyGridNavigator

GreedyGridNavigator is defined in gridnavigator.py. The
GreedyGridNavigator does two things. First, it creates a grid-based path
network, as described above. Second, it causes the Agent to navigate to
a destination by trying to find the neighbor (left, right, up, down)
that is closest to the destination. Greedy navigation may fail, so the
path terminates after 100 cells at which point the Agent moves directly
to its destination from the last point reached. Thus, the Agent can
possibly collide with obstacles if the greedy path does not reach the
destination before the threshold is reached.

Member functions:

  - computePath(source, destination): Find a path through the grid
    (causing path to be not None) and call back to the Agent to start
    moving. The path is created by finding the closest cell to the
    source and then selecting successor cell that move the agent closer
    to the destination until the closest cell to the destination is
    found. If the path length exceeds 100, then the Agent will be sent
    to its destination without further collision avoidance.

### Miscellaneous utility functions

Miscellaneous utility functions are found in utils.py.

  - distance(point1, point2): returns the distance between two points.
    Points are tuples of the form (x, y).
  - calculateIntersectPoint(point1, point2, point3, point4): returns a
    point (x, y) at the intersection of two lines, or None if the lines
    are parallel. One line is between point1 and point2 and the other
    line between point3 and point4.
  - rayTrace(point1, point2, line): returns the intersection point (x,
    y) if a beam between point1 and point2 crosses the given line.
  - rayTraceWorld(point1, point2, worldlines): performs a ray trace
    against every line in worldlines and returns the first intersection
    point found. worldlines is a list of lines of the form ((x1, y1),
    (x2, y2)).
  - rayTraceNoEndpoints(point1, point2, line): same as rayTrace(), but
    doesn't check collisions with the end points of the two lines.
  - rayTraceWorldNoEndpoints(point1, point2, worldlines): same as
    rayTraceWorld(), but doesn't check end points of any lines compared
    against each other.
  - pointInsidePolygonPoints(point, listofpoints): returns True if point
    is within a polygon defined by listofpoints. Points are tuples of
    form (x, y).
  - pointInsidePolygonLines(point, lines): returns True if point is
    within a polygon defined by lines. The point is of the form (x, y).
    Lines is a list of tuples of the form ((x1, y1), (x2, y2)).
  - drawCross(surface, point, color, size, width): draw a cross on a
    PyGame drawing surface. Point is the center of the cross, a tuple of
    the form (x, y). Color is a tuple of the form (red, green, blue)
    with values between 0 and 255, each. size is the length of the lines
    in the cross. width is the width of the lines.

-----

## Instructions

You must superimpose a grid over an arbitrary, given game world terrain
consisting of obstacles. The grid is a 2D array of booleans such that a
False in any particular cell means the Agent cannot walk into the cell
and a True in any particular cell means the Agent can walk into the
cell. We have provided two different types of Navigator:
RandomGridNavigator and GreedyGridNavigator. Neither are guaranteed to
deliver an Agent to their final, desired destination.

When you click on the screen, you indicate where you want the Agent to
traverse.

**Step 1:** Download and install the game engine. This must be done in
two parts. First, you must install PyGame, the underlying rendering
engine. Follow the instructions for Windows, Mac, and Linux found in the
zip file. See the [installation instructions](installation.html).

**Step 2:** Verify the installation is successful by running the game
engine:

You should see a top-down view of the game world, consisting of some
obstacles (black polygons), some resources (crystal sprites), and an
agent. This agent is the player avatar, meaning it is controlled by the
player. When you click on a point on the screen, the agent will proceed
directly there. runbasic.py uses the base Navigator class, which does
not avoid collisions.

**Step 3:** Run the grid navigator code:

You will see the same thing as before with runbasic.py. However, when
you click on the screen, the agent will not move. This agent uses
RandomGridNavigator, which must first be completed by you.

**Step 4:** Modify mycreategrid.py and complete the myCreateGrid()
function. myCreateGrid() must do two things:

1.  It must create and return a 2D array of booleans such that
    grid\[column\]\[row\] indicates the traversability of the cell at
    (column, row).
2.  It must returns the dimensions of the 2D array in the form of
    (num\_columns, num\_rows).

The inputs to myCreateGrid are: a reference to the GameWorld and the
cell size, which indicates the width and height of each cell. Grid cells
can touch the borders of the game world. That is, a cell can have its
upper left corner at point (0, 0).

**Step 5:** Test your implementation:

Additional testing can be done by making your own maps.

-----

## Grading

This homework assignments is worth 5 points. Your solution will be
graded by autograder. The autograder will look for grid cells that
intersect with obstacles. For every map that your solution is tested
against, 1 point will be deducted if at least one cell intersects with
an obstacle. The autograder will test your solution on 5 maps, three of
which are provided as test maps.

-----

## Hints

Debugging within the game engine can be hard. Print statements will be
one possible way of figuring out what is going on.

It can also be helpful to draw debugging information, such as lines and
points, to the screen.

To draw a cross on the screen use the following:

In general, you should be able to get all the data you need from the
GameWorld, Obstacles objects, and the Agent through getter functions. If
you find yourself directly accessing member variables of other objects,
you may want to rethink your approach.

It is good to test your techniques on new maps. If you want to make new
maps, make a copy of one of the run\*.py files and edit the call to
world.initializeTerrain(). initializeTerrain(polygons, color, linewidth,
sprite) instantiates the physical Obstacle objects (specifically
ManualObstacle objects) in a game. A list of polygons is given, such
that there is one polygon for each obstacle. A polygon is a list of
points where a point is a tuple of the form (x, y). The color of the
line is given, in the form (red, green, blue) where each values is
between 0 and 255. The default color is black (0, 0, 0). Linewidth
indicates how thick to make the line of the polygon. Obstacles will be
filled with repeating sprites if the optional sprite parameter is given
as a string pathname to an image file.

Sometimes the game world is larger than the screen resolution of a
computer. The size of the screen is independent of the size of the game
world. GameWorld can be initialized with three parameters. The first is
a seed to help reproduce random values. If seed is None, the current
system time is used as the seed. The second is the dimensions of the
world in the form (x, y). The third is the dimensions of the screen in
the form (x, y). The dimensions of the screen should be equal to or
smaller than the dimensions of the world.

-----

## Submission

To submit your solution, upload your modified mycreategrid.py. All work
should be done within this file.

You should not modify any other files in the game engine.

DO NOT upload the entire game engine.