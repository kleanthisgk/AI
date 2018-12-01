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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        #if action is not to move return -inf
        if action == Directions.STOP:
            return float("-inf")

        #A quick and efficient way to to evaluate an action is to find the distance to closest food and add the reciprocal of it to score.
        #The number is bigger the closest we are to eating food
        minFood = 9999
        for food in newFood.asList():
            dist = util.manhattanDistance(newPos, food)
            if dist < minFood:
                minFood = dist

        return 1.0/minFood + successorGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

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
        return self.maxFunction(gameState, 0)  # returns the best action for pacman and starts at depth 0
        util.raiseNotDefined()

    def maxFunction(self, state, depth):  # takes gamestate and depth
        if state.isWin() or state.isLose() or depth == self.depth:  # it returns the evaluation function if state is terminal or depth is depth of the tree
            return self.evaluationFunction(state)

        maxValue = float("-inf")
        maxAction = []

        for action in state.getLegalActions(0):  # gets all actions for pacman who is agent 0
            v = self.minFunction(state.generateSuccessor(0, action), depth, 1)  # calls minFunction for the first ghost agent who is 1

            if v > maxValue:  # takes the max value of all mins and the best action
                maxValue = v
                maxAction = action

        if depth == 0:  # if we are at depth 0 it means that we have to return the right action
            return maxAction
        else:  # else we return the max value
            return maxValue

    def minFunction(self, state, depth, agent):  # takes the gamestate, the depth and the agent
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        minValue = float("inf")

        for action in state.getLegalActions(agent):
            if agent == state.getNumAgents() - 1:  # agent is the last ghost agent and the next one is pacman
                v = self.maxFunction(state.generateSuccessor(agent, action), depth + 1)  # we call maxfunction for pacman at the next depth
            else:  # there are more ghost agents
                v = self.minFunction(state.generateSuccessor(agent, action), depth, agent + 1)  # we go on the next agent on the same depth

            if v < minValue:  # we take the min value
                minValue = v

        return minValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.maxFunction(gameState, 0, float("-inf"),
                                float("inf"))  # returns the best action for pacman and starts at depth 0
        # with a as -inf and b as inf
        util.raiseNotDefined()

    def maxFunction(self, state, depth, a, b):  # takes gamestate, depth, a and b
        if state.isWin() or state.isLose() or depth == self.depth:  # it returns evaluation function if state is terminal or depth is depth of the tree
            return self.evaluationFunction(state)

        maxValue = float("-inf")
        maxAction = []

        for action in state.getLegalActions(0):  # gets all actions for pacman who is agent 0
            v = self.minFunction(state.generateSuccessor(0, action), depth, 1, a, b)  # calls minFunction for the first ghost agent who is 1

            if v > maxValue:  # takes the max value of all mins and the best action
                maxValue = v
                maxAction = action

            if maxValue > b:  # if max value is greater than b then we return that value
                return maxValue

            a = max(a, v)  # a is the biggest number from a and v

        if depth == 0:  # if we are at depth 0 it means that we have to return the right action
            return maxAction
        else:  # else we return the max value
            return maxValue

    def minFunction(self, state, depth, agent, a, b):  # takes the gamestate, the depth, the agent, a and b
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        minValue = float("inf")

        for action in state.getLegalActions(agent):
            if agent == state.getNumAgents() - 1:  # agent is the last ghost agent and the next one is pacman
                v = self.maxFunction(state.generateSuccessor(agent, action), depth + 1, a, b)  # we call maxfunction for pacman at the next depth
            else:  # there are more ghost agents
                v = self.minFunction(state.generateSuccessor(agent, action), depth, agent + 1, a, b)  # we go on the next agent on the same depth

            if v < minValue:  # we take the min value
                minValue = v

            if minValue < a:  # if min value is < than a then we return that number
                return minValue

            b = min(b, v)  # b is the smallesr number of b and v

        return minValue


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxFunction(gameState, 0)  # returns the best action for pacman and starts at depth 0
        util.raiseNotDefined()

    def maxFunction(self, state, depth):  # takes gamestate and depth
        if state.isWin() or state.isLose() or depth == self.depth:  # it returns evaluation function if state is terminal or depth is depth of the tree
            return self.evaluationFunction(state)

        maxValue = float("-inf")
        maxAction = []

        for action in state.getLegalActions(0):  # gets all actions for pacman who is agent 0
            v = self.expectFunction(state.generateSuccessor(0, action), depth, 1)  # calls minFunction for the first ghost agent who is 1

            if v > maxValue:  # takes the max value of all mins and the best action
                maxValue = v
                maxAction = action

        if depth == 0:  # if we are at depth 0 it means that we have to return the right action
            return maxAction
        else:  # else we return the max value
            return maxValue

    def expectFunction(self, state, depth, agent):  # takes the gamestate, the depth and the agent
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        sumValue = 0
        for action in state.getLegalActions(agent):
            if agent == state.getNumAgents() - 1:  # agent is the last ghost agent and the next one is pacman
                # we sum every value of the children of each node and at the end we divide by the amount of child nodes
                sumValue += self.maxFunction(state.generateSuccessor(agent, action), depth + 1)  # we call maxfunction for pacman at the next depth
            else:  # there are more ghost agents
                sumValue += self.expectFunction(state.generateSuccessor(agent, action), depth, agent + 1)  # we go on the next agent on the same depth

        expectValue = float(sumValue) / len(state.getLegalActions(agent))

        return expectValue


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #A quick and efficient way to to evaluate a state is to find the distance to closest food and add the reciprocal of it to score.
    #The number is bigger the closest we are to eating food
    currPos = currentGameState.getPacmanPosition()
    currFood = currentGameState.getFood()

    minFood = 9999
    for food in currFood.asList():
        dist = util.manhattanDistance(currPos, food)
        if dist < minFood:
            minFood = dist

    return 1.0 / minFood + currentGameState.getScore()
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
