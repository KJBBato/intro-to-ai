# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # Initialize visitedSet, currentState, stateStack
    visitedPathSet = []
    currentState = (problem.getStartState(), [], None)
    stateStack = util.Stack()

    # Initially, startState is the first to be in stack
    stateStack.push(currentState)

    # Loops while stack is not empty   
    while(not(stateStack.isEmpty())):

        # takes currentState from the top of the stack
        currentState = stateStack.pop()
        state, path, direction = currentState[0], currentState[1], currentState[2]
        
        # if the state is a goalState then return path
        if problem.isGoalState(state):
            return path

        # If state is not visited, visit it 
        if state not in visitedPathSet:

            # updates visitedSet
            visitedPathSet.append(state)

            # go through all successors in the list
            for successor in list(problem.getSuccessors(state)):

                # push to stack iff that successor was not visited
                if successor[0] not in visitedPathSet:
                    stateStack.push((successor[0], path + [successor[1]], successor[1]))
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    # Initialize visitedSet, currentState, stateQueue
    visitedPathSet = []
    currentState = (problem.getStartState(), [], None)
    stateQueue = util.Queue()

    # Initially, startState is the first to be in queue
    stateQueue.push(currentState)

    # Loops while queue is not empty
    while(not(stateQueue.isEmpty())):

        # takes currentState from the beginning of queue
        currentState = stateQueue.pop()
        state, path, direction = currentState[0], currentState[1], currentState[2]

        # if the state is a goalState then return path
        if problem.isGoalState(state):
            return path

        # If state is not visited, visit it 
        if state not in visitedPathSet:

            # updates visitedSet
            visitedPathSet.append(state)

            # go through all successors in the list
            for successor in list(problem.getSuccessors(state)):

                # push to queue iff that successor was not visited
                if successor not in visitedPathSet:
                    stateQueue.push((successor[0], path + [successor[1]],
                     successor[1])) 

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # Initialize visitedSet, currentState, stateQueue
    visitedPathSet = []
    currentState = (problem.getStartState(), [], None, 0)
    stateQueue = util.PriorityQueue()

    # Initially, startState is the first to be in queue
    stateQueue.push(currentState, 0)

    # Loops while queue is not empty
    while(not(stateQueue.isEmpty())):

        # takes currentState from the beginning of queue
        currentState = stateQueue.pop()
        state, path, direction, cost = currentState[0], currentState[1], currentState[2], currentState[3]

        # if the state is a goalState then return path
        if problem.isGoalState(state):
            return path

        # If state is not visited, visit it 
        if state not in visitedPathSet:

            # updates visitedSet
            visitedPathSet.append(state)

            # go through all successors in the list
            for successor in list(problem.getSuccessors(state)):

                # push to queue iff that successor was not visited
                if successor not in visitedPathSet:
                    stateQueue.push((successor[0], path + [successor[1]], successor[1], successor[2] + cost),
                     successor[2] + cost) 

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    # Initialize visitedSet, currentState, stateQueue
    visitedPathSet = []
    currentState = (problem.getStartState(), [], None, 0)
    stateQueue = util.PriorityQueue()

    # Initially, startState is the first to be in queue
    stateQueue.push(currentState, 0 )

    # Loops while queue is not empty
    while(not(stateQueue.isEmpty())):

        # takes currentState from the beginning of queue
        currentState = stateQueue.pop()
        state, path, direction, cost = currentState[0], currentState[1], currentState[2], currentState[3]

        # if the state is a goalState then return path
        if problem.isGoalState(state):
            return path

        # If state is not visited, visit it 
        if state not in visitedPathSet:

            # updates visitedPathSet
            visitedPathSet.append(state)

            # go through all successors in the list
            for successor in list(problem.getSuccessors(state)):

                # push to queue iff that successor was not visited
                if successor not in visitedPathSet:
                    h = heuristic(successor[0], problem)
                    stateQueue.push((successor[0], path + [successor[1]], successor[1], successor[2] + cost),
                     successor[2] + cost + h) 

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
