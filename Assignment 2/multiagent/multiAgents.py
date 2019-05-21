# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        """ Debug Prints
        print "Successor State: "
        print successorGameState
        print "New Position: ", newPos
        print "Successor Ghost States: ", successorGameState.getGhostPositions()
        print "New Scared Timer: ", newScaredTimes 
        print "Food Grid: "
        print newFood.asList()
        print
        """

        mDistancePGList, mDistancePFList = [], []

        for ghost in successorGameState.getGhostPositions():
          mDistancePGList.append(util.manhattanDistance(newPos, ghost))

        mDistancePG = min(mDistancePGList) + 1

        for food in newFood.asList():
          mDistancePFList.append(util.manhattanDistance(newPos, food))

        if not successorGameState.isWin():
          mDistancePF = min(mDistancePFList) + 1
        else:
          mDistancePF = 1

        if mDistancePG > 2:
          overallScore = successorGameState.getScore() + float(-85/mDistancePG) + float(20/mDistancePF)
        else:
          overallScore = mDistancePG

        return overallScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    ##### Private methods specifically for Minimax Agent #####
    def _getValue(self, state, currentDepth, maxDepth, currentAgent):
      if state.isWin() or state.isLose() or currentDepth == maxDepth:
        return self.evaluationFunction(state)
      
      # Next agent
      nextAgent = (currentAgent + 1) % state.getNumAgents()
      newDepth = currentDepth + 1
      # If agent is pacman
      if nextAgent == 0:
        return self._getMaxValue(state, newDepth, maxDepth, nextAgent)
      # must be ghost
      else: 
        return self._getMinValue(state, newDepth, maxDepth, nextAgent)

    def _getMaxValue(self, state, currentDepth, maxDepth, currentAgent):
      maxVal = float("-inf")
      actionList = state.getLegalActions(currentAgent)
      for action in actionList:
        successorState = state.generateSuccessor(currentAgent, action)
        maxVal = max(maxVal, self._getValue(successorState, currentDepth, maxDepth, currentAgent))
      return maxVal

    def _getMinValue(self, state, currentDepth, maxDepth, currentAgent):
      minVal = float("inf")
      actionList = state.getLegalActions(currentAgent)
      for action in actionList:
        successorState = state.generateSuccessor(currentAgent, action)
        minVal = min(minVal, self._getValue(successorState, currentDepth, maxDepth, currentAgent))
      return minVal

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        """
        print "Legal Actions from Pacman: ", gameState.getLegalActions(self.index)   
        print
        print "Number of Agents: ", gameState.getNumAgents()
        """

        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)

        maxDepth = self.depth * gameState.getNumAgents()
        bestMove = None
        actionList = gameState.getLegalActions(self.index)
        maxVal = float("-inf")

        for action in actionList:
          successorState = gameState.generateSuccessor(self.index, action)
          overallScore = self._getValue(successorState, 1, maxDepth, self.index)
          if overallScore > maxVal:
            maxVal, bestMove = overallScore, action
        return bestMove

    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    ##### Private methods specifically for Minimax Agent with Alpha-Beta Pruning #####
    def _getValue(self, state, currentDepth, maxDepth, currentAgent, alpha, beta):
      if state.isWin() or state.isLose() or currentDepth == maxDepth:
        return self.evaluationFunction(state)

      nextAgent = (currentAgent + 1) % state.getNumAgents()
      newDepth = currentDepth + 1
      if nextAgent == 0:
        return self._getMaxValue(state, newDepth, maxDepth, nextAgent, alpha, beta)
      else:
        return self._getMinValue(state, newDepth, maxDepth, nextAgent, alpha, beta)

    def _getMaxValue(self, state, currentDepth, maxDepth, currentAgent, alpha, beta):
      maxVal = float("-inf")
      actionList = state.getLegalActions(currentAgent)
      for action in actionList:
        successorState = state.generateSuccessor(currentAgent, action)
        maxVal = max(maxVal, self._getValue(successorState, currentDepth, maxDepth, currentAgent, alpha, beta))
        if maxVal >= beta:
          return maxVal
        alpha = max(maxVal, alpha)
      return maxVal

    def _getMinValue(self, state, currentDepth, maxDepth, currentAgent, alpha, beta):
      minVal = float("inf")
      actionList = state.getLegalActions(currentAgent)
      for action in actionList:
        successorState = state.generateSuccessor(currentAgent, action)
        minVal = min(minVal, self._getValue(successorState, currentDepth, maxDepth, currentAgent, alpha, beta))
        if minVal <= alpha:
          return minVal
        beta = min(minVal, beta)
      return minVal


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)

        maxDepth = self.depth * gameState.getNumAgents()
        bestMove = None
        actionList = gameState.getLegalActions(self.index)
        maxVal = float("-inf") 

        for action in actionList:
          successorState = gameState.generateSuccessor(self.index, action)
          overallScore = self._getValue(successorState, 1, maxDepth, self.index, maxVal, float("inf"))
          if overallScore > maxVal:
            maxVal, bestMove = overallScore, action
        return bestMove
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    ##### Private methods specifically for Expectimax Agent #####
    def _getValue(self, state, currentDepth, maxDepth, currentAgent):
      # Base Case
      if state.isWin() or state.isLose() or currentDepth == maxDepth:
        return self.evaluationFunction(state)
      
      # Next agent
      nextAgent = (currentAgent + 1) % state.getNumAgents()
      newDepth = currentDepth + 1
      # If agent is pacman
      if nextAgent == 0:
        return self._getMaxValue(state, newDepth, maxDepth, nextAgent)
      # must be ghost
      else: 
        return self._getMinValue(state, newDepth, maxDepth, nextAgent)

    def _getMaxValue(self, state, currentDepth, maxDepth, currentAgent):
      maxVal = float("-inf")
      actionList = state.getLegalActions(currentAgent)
      for action in actionList:
        successorState = state.generateSuccessor(currentAgent, action)
        maxVal = max(maxVal, self._getValue(successorState, currentDepth, maxDepth, currentAgent))
      return maxVal

    def _getMinValue(self, state, currentDepth, maxDepth, currentAgent):
      sumValue, length = 0, 0 
      actionList = state.getLegalActions(currentAgent)
      for action in actionList:
        successorState = state.generateSuccessor(currentAgent, action)
        sumValue += float(self._getValue(successorState, currentDepth, maxDepth, currentAgent))
        length += 1.0
      avg = float(sumValue/length)
      return avg

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)

        maxDepth = self.depth * gameState.getNumAgents()
        bestMove = None
        actionList = gameState.getLegalActions(self.index)
        maxVal = float("-inf")

        for action in actionList:
          successorState = gameState.generateSuccessor(self.index, action)
          overallScore = self._getValue(successorState, 1, maxDepth, self.index)
          if overallScore > maxVal:
            maxVal, bestMove = overallScore, action
        return bestMove

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Incorporated my old evaluation function from above and tried to
        add in the scare timer as a part of the score.
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    mDistancePGList, mDistancePFList = [], []

    """
    if newScaredTimes[0] > 0:
      scareScore = 0
    else:
      scareScore = 10000
    """

    for ghost in currentGameState.getGhostPositions():
      mDistancePGList.append(util.manhattanDistance(newPos, ghost))

    mDistancePG = min(mDistancePGList) + 1

    for food in newFood.asList():
      mDistancePFList.append(util.manhattanDistance(newPos, food))

    if not currentGameState.isWin():
      mDistancePF = min(mDistancePFList) + 1
    else:
      mDistancePF = 1

    if mDistancePG > 2:
      overallScore = currentGameState.getScore() + float(-90/mDistancePG) + float(20/mDistancePF) 
    else:
      overallScore = mDistancePG

    return overallScore

# Abbreviation
better = betterEvaluationFunction

