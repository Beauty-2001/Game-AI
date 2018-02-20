# Homework 5: Minion Agents

A [Multiplayer Online Battle Arena (MOBA)](http://en.wikipedia.org/wiki/Multiplayer_online_battle_arena) is a form of Real-Time Strategy game in which the player controls a powerful agent called the "Hero" in a world populated with simple, weak, fully computer-controlled agents called "Minions." In this assignment, we will implement the decision-making for Minion agents.

A MOBA has two teams. Each team has a base, which is protected by a number of towers. The goal is to destroy the opponent's base. In MOBAs, bases periodically spawn Minion agents, who automatically attack the enemy towers and bases. Towers and bases can defend themselves; they target Minions before targeting Heroes. Thus Minions provide cover for Heroes, who are much more powerful.

In this assignment, you will implement a MOBA that only has Minions (no Heroes).

[![](moba1.png)](moba1.png)

Typically in a MOBA there are three routes Minions can follow to get to the enemy base—a route through the center with a large melee area, and two routes around the edges of the map—and minions would randomly follow one path. In the MOBA we are building, minions will use A* to follow the shortest path. Gates will randomly appear, sometimes blocking a route and Minions will need to plan paths along alternate routes. There will always be one route open. We will build off your previous navigation mesh and path network generation solution from **homework 3** and your previous A* implementation from **homework 4**.

Minion decision-making is as follows. If there are towers, Minions automatically navigate to within attacking distance of an enemy tower. If there are no enemy towers, Minions automatically navigate to within attacking distance of enemy bases. Minions can shoot at towers, bases, and enemy agents. Targets are prioritized as follows: closest enemy tower, closest enemy base, closest enemy minion, closest enemy hero.

The bases will automatically spawn Minion agents, after a fixed interval of time; bases will be limited in the number of Minions that can be alive at any given time. Bases are invulnerable as long as there are towers remaining, so towers must be targeted and destroyed first.

In this assignment, you will implement a Finite State Machine (FSM) for Minion agents. The base Minion class has state machine running code built into it and each state is an object that implements the behavior of the agent in that state by telling the agent what to do and where to go. Specifically, states have code in their execute() functions that act as the decision-making "brain" of the Minion, instructing it what to do at every tick of the game. The Minion agent class will automatically start off in an Idle state. You must implement at least two other states, and modify the Idle state to immediately transition to one of the other states you have implemented.

Recommended states for a Minion are: move, attack tower, attack base, attack enemy minion, attack enemy hero. These are suggestions and not all are strictly necessary.

You must implement Minion AI that can win the game by destroying the enemy base.

* * *

## What you need to know

Please consult previous homework instructions for background on the Game Engine. In addition to the information about the game engine provided there, the following are new elements you need to know about.

### Agent

Three things are newly relevant to this assignment. (1) Agents have hitpoints. (2) Agents can be part of a team. (3) Agents can shoot in the direction they are facing.

Member variables:

*   hitpoints: the amount of health the agent has. The agent dies when hitpoints reaches zero.
*   team: the symbolic name of the team the agent is on.

Member functions:

*   getHitpoints(): returns the number of hitpoints.
*   getTeam(): returns the symbol of the team the agent is on.
*   turnToFace(pos): turn the agent to face a particular point (x, y)
*   shoot(): fire the agent's gun in the direction the agent is facing. The agent can only fire after a certain number of ticks have elapsed.

Note: To shoot at something, first turn the agent to face the target (or to the point the agent wishes to fire at) with turnToFace() and then call shoot().

### StateMachine

A StateMachine implements the generic functionality of a Finite State Machine. In this assignment, StateMachine is one of the base classes of Minions, thus every Minion is a StateMachine. StateMachines know what the current state is and tell the current state to execute at every update.

Member variables:

*   states: A list of states that the machine can be in. States are names of classes that subclass State. Only States that are in this list can be executed.
*   state: A pointer to the current state instance.

Member functions:

*   getState(): returns the type of the current state. Since it is usually not important to have a pointer to the state object, getState() returns the type of the current state. Thus, if you want to know what the StateMachine is doing, use something like: getState() == Idle
*   update(delta): Should be called every tick. This will be called by the engine's game loop. The current state will have its execute() function called. Delta is the amount of time that has passed since the last tick.
*   changeState(newclass, *args): causes the StateMachine to change state. newclass is the type of the state to run next, which will be instantiated. Sometimes states take arguments, so pass in any arguments through *args. changeState takes an arbitrary number of arguments after the first one. Only the first argument is required.

Note: A StateMachine will not change states to any type of state that is not listed in StateMachine.states.

### State

An abstract base class for all states in a StateMachine. States are more than symbols. Each state has an execute() function that gets called every tick of the game and controls the behavior of the agent.

Member variables:

*   agent: A reference to the agent that this state is controlling.

Member functions:

*   enter(oldstate): this function is called when the state begins execution. A state should do whatever one-time work is necessary to set things up for execution. oldstate is the type of the state that executed just prior to the state change.
*   execute(delta): does the work of controlling the agent. Delta is the amount of time elapsed since the last call to execute. This function is part of the game loop update, so should not perform computationally expensive operations. Delta is the amount of time that has passed since the last tick.
*   exit(): this function is called when the agent is about to transition to another state. Use this function to do any clean up of data structures or final instructions to the agent.
*   parseArgs(args): you can override this function to take any arguments passed into the state upon creation and do the right thing with them.

For execute() to control the agent, it must make call-backs via the agent member variables. For example, if the behavior of a state is to make the agent shoot, the execute() function can call self.agent.shoot(). To change states, call back to self.agent.changeState(new_state_type).

When changeState() is called, arguments can be passed to the new state when it is initialized. The constructor for the base State class takes a number of arguments, as a list. But it doesn't know what they are meant to be. Constructors for sub-classes can look at the arguments passed in through args and pick out the relevant information and store it or compute with it. For example, one might want a **Taunt** state, and pass in an argument for the thing to be taunted. For example: the agent could call self.changeState(Taunt, enemyagent). Even though the Taunt sub-class is expecting an argument, it will just be passed in to the constructor as args[0]. Use parseArgs(args) to capture the parameter and use it. For example:

### StateAgent

A StateAgent is a sub-class of Agent and StateMachine. Use getStateType() to determine what state the agent is in.

### VisionAgent

A VisionAgent is a sub-class of StateAgent. VisionAgent is given a viewangle, a number of degrees that the agent can see. Every tick, the VisionAgent asks the GameWorld what it can see, based on its view angle, and maintains a list of visible Movers (agents, bullets, towers, and bases). For this assignment, Minions have a view angle of 360 degrees, meaning they can see everything around them irrespective of what direction they are facing.

Member variables:

*   viewangle: the number of degrees the agent can see, centered around the front of the agent (i.e., 1/2 viewangle clockwise from the agent's orientation, and 1/2 viewangle counterclockwise from the agent's orientation).
*   visible: a list of Movers that is currently visible (re-computed every tick).

Member functions:

*   getVisible(): returns a list of visible Movers.
*   getVisibleType(type): returns a list of visible Movers of a given class type.

### MOBAAgent

A sub-class of VisionAgent (and hence also a StateAgent and a StateMachine), specialized for the MOBA. MOBAAgents do two noteworthy things. First, **MOBAAgents die whenever they collide with an Obstacle**. Second, they can compute a list of points in navigable space in the event that the agent needs to choose a point to move to without worrying about whether that point is inside an Obstacle (the agent will still have to figure out if it can actually move there).

Member variables:

*   maxHitpoints: the maximum number of hitpoints the agent can have.

Member functions:

*   getMaxHitpoints(): returns the maximum number of hitpoints the agent can have.
*   getPossibleDestinations(): returns a list of points that are not in Obstacles.

### Minion

Abstract base class of MyMinion, which is a sub-type of MOBAAgent. Otherwise doesn't add any functionality.

### Hero

Abstract base class, which is a sub-type of MOBAAgent. Otherwise doesn't add any functionality. The player-controlled agent is a Hero.

### MOBABullet

A special Bullet class for the MOBA. MOBABullets differ from regular bullets in that they are range-limited.

There are four sub-classes of MOBABullet: SmallBullet, BigBullet, BaseBullet, and TowerBullet. These bullets are specific to Minions, Heroes, Bases, and Towers, respectively and do different amounts of damage.

### Base

Each team in a MOBA has a Base. Bases spawn minions at regular intervals as long as the maximum number of minions allowed at any given time has not been reached. Bases cannot be damaged as long as there are towers present on the same team. Bases can heal Heroes—if a Hero touches a base, its hitpoints are restored to maximum value.

Member variables:

*   team: the symbol of the team that the base is on.
*   hitpoints: the amount of health the base has.

Member functions:

*   getTeam(): returns the symbol of the team the base is on.
*   getHitpoints(): returns the number of hitpoints.

### Tower

Bases are defended by towers, which will shoot at the closest unit of the enemy team. Towers will prioritize minions over heros when selecting targets to shoot at.

Member variables:

*   team: the symbol of the team that the base is on.
*   hitpoints: the amount of health the tower has.

Member functions:

*   getTeam(): returns the symbol of the team the base is on.
*   getHitpoints(): returns the number of hitpoints.

### MOBAWorld

A special type of GameWorld for MOBAs. MOBAWorld is a type of GatedWorld. The MOBAWorld keeps track of bases and towers, in addition to NPCs, Bullets, and the agent.

Member functions:

*   getNPCs(): returns a list of NPCs in the game (includes all agents not controlled by the player).
*   getNPCsForTeam(team): return a list of NPCs part of the given team.
*   getEnemyNPCs(myteam): return a list of NPCs that are not part of the given team.
*   getAgent(): returns the player-controlled character.
*   getBases(): return a list of all bases.
*   getBasesForTeam(team): return a list of all bases on a given team.
*   getEnemyBases(team): return a list of all bases not on the given team.
*   getTowers(): return a list of all towers.
*   getTowersForTeam(team): return a list of all towers on a given team.
*   getEnemyTowers(team): return a list of all towers not on the given team.
*   getBullets(): return a list of all bullets in the world at that moment.

* * *

## Instructions

To complete this assignment, you must implement Minion AI. Write at least two State classes, and modify the Idle state class to transition to these customized states.

Use your solution to **homework 3** to generate a navigation mesh and a corresponding path network. The instructor can provide you with a default solution if necessary. You may also wish to use any path smoothing operations from **homework 4**. Use your A* implementation from **homework 4**. The instructor can provide you with a default solution if necessary.

To run the project code, use runmobacompetition.py to run different Minion types against each other. Example calls are:

**> python runmobacompetition.py MyMinion MyMinion  
> python runmobacompetition.py My**
**Minion BaselineMinion  
> python runmobacompetition.py BaselineMinion BaselineMinion  
**

BaselineMinion is a bare-bones implementation of Minion AI that you can use to test against. BaselineMinion agents simply navigate to the nearest tower (or base if there are no remaining towers) and shoot.

The following steps are required to complete the assignment.

**Step 1:** Copy your myCreatePathNetwork function from homework 3\.

**Step 2:** Copy your astarnavigator.py from homework 4\. Copy mynavigatorhelpers.py functions from homework 4.

**Step 3:** Implement at least two classes in MyMinion.py that sub-class from State. Implement their enter(), exit(), execute(), constructors, and parseArgs() as necessary. You must create at least two states (in addition to Idle).

**Step 4:** Modify the execute() function in the Idle class in MyMinion.py. Minions automatically start in the Idle state. The main purpose of the Idle class is to transition to another state.

**Step 5:** Modify the constructor of MyMinion in MyMinion.py to add any new states to self.states. States cannot be executed unless they are in self.states. Make sure you do not remove Idle from the list of states.

* * *

## Grading

The instructor will provide a baseline opponent, BaselineMinion, which is a simple implementation of minion AI in which a minion navigates directly to the nearest tower (or base if all towers are destroyed) and shoots as soon as within range.

The following grading criteria will be used:

*   7 points: Kill the enemy base with fewer than 60 minions when playing against the baseline agent. One point deducted for each additional 3 minions needed.
*   3 points: Kill the enemy base before the baseline opponent. Three matches will be played, one point earned per match won.

Games will be run from both sides of the map and the best result will be taken.

Submissions will receive no points if they do not implement and use at least two states.

* * *

## Hints

The player-controlled character is a Hero with team=0\. You can use the player-controlled Hero to test whether your minions differentiate Heroes from other NPCs. Note that the player character is not in MOBAWorld.getNPCs(), so if you want to target the player-controlled character you may want to assemble a list of targets; i.e., targets = world.getEnemyNPCs(team) + [world.getAgent()]

Use agent.getVisible() and agent.getVisibleType() to figure out what the agent can shoot at.

Remember, an agent shoots in the direction it is facing, so use agent.turnToFace(enemy) before agent.shoot().

* * *

## Submission

To submit your solution, upload your modified MyMinion.py, mycreatepathnetwork.py, astarnavigator.py, and mynavigatorhelpers.py.

You should not modify any other files in the game engine.

DO NOT upload the entire game engine.