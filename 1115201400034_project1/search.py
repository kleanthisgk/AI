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
    "*** YOUR CODE HERE ***"
    class Node:
        def __init__(self, state, parent, action, pathCost):
            self.state = state #state of the game
            self.parent = parent #parent of the node
            self.action = action #action that led to that node
            self.pathCost = pathCost #total cost of tha path until that node

        def solution(self): #return the path to the goal node
          path = [] #path is a list of actions
          tempNode = self #temp node is the goal node
          while tempNode.state != problem.getStartState(): #until we get to the initial node
              path.insert(0, tempNode.action) #insert at the start of the list
              tempNode = tempNode.parent #go to the parent of the node
          return path #return list of actions

    def childNode(successor, parent, action, stepCost):
        pathCost = parent.pathCost + stepCost #total cost is the total cost of the parent + the cost of the last action
        child = Node(successor, parent, action, pathCost) #create new child node
        return child

    initialNode = Node(problem.getStartState(), None, None, 0) #create initial node with start state and no parent
    if problem.isGoalState(initialNode.state):
        return initialNode.solution()

    frontier = util.Stack() #dfs uses a stack
    frontier.push(initialNode) #insert initial node to the stack
    explored = set() #explored nodes are added to a set

    while not frontier.isEmpty(): #while stack is not empty
        nextNode = frontier.pop() #extract the last node entered
        explored.add(nextNode.state) #add the state of the node to the explored set
        for successor, action, stepCost in problem.getSuccessors(nextNode.state): #for every successor create a new child
            child = childNode(successor, nextNode, action, stepCost)
            if child.state not in explored and child not in frontier.list: #if child is not already explored or is not in the stack
                if problem.isGoalState(child.state):  # if node is goal node we return the path of actions
                    return child.solution()
                frontier.push(child) #insert it into the stack

    return [] #if stack is empty
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    class Node:
        def __init__(self, state, parent, action, pathCost):
            self.state = state
            self.parent = parent
            self.action = action
            self.pathCost = pathCost

        def solution(self):
          path = list()
          tempNode = self
          while tempNode.state != problem.getStartState():
              path.insert(0, tempNode.action)
              tempNode = tempNode.parent
          return path




    def childNode(successor, parent, action, stepCost):
        pathCost = parent.pathCost + stepCost
        child = Node(successor, parent, action, pathCost)
        return child

    initialNode = Node(problem.getStartState(), None, None, 0)
    if problem.isGoalState(initialNode.state):
        return initialNode.solution()

    frontier = util.Queue() #bfs uses a queue
    frontier.push(initialNode)
    explored = set()

    while not frontier.isEmpty() :
        nextNode = frontier.pop() #extract from the start of the queue
        explored.add(nextNode.state)
        for successor, action, stepCost in problem.getSuccessors(nextNode.state):
            child = childNode(successor, nextNode, action, stepCost)
            if child.state not in explored and child not in frontier.list:
                if problem.isGoalState(child.state):
                    return child.solution()
                frontier.push(child)
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    class Node:
        def __init__(self, state, parent, action, pathCost):
            self.state = state
            self.parent = parent
            self.action = action
            self.pathCost = pathCost

        def solution(self):
          path = list()
          tempNode = self
          while tempNode.state != problem.getStartState():
              path.insert(0, tempNode.action)
              tempNode = tempNode.parent
          return path

        def __eq__(self, other):
            if isinstance(other, Node):
                return self.state == other.state


    def childNode(successor, parent, action, stepCost):
        pathCost = parent.pathCost + stepCost
        child = Node(successor, parent, action, pathCost)
        return child

    initialNode = Node(problem.getStartState(), None, None, 0)
    frontier = util.PriorityQueue() #ucs uses a priority queue
    frontier.push(initialNode, initialNode.pathCost)
    explored = set()

    while not frontier.isEmpty() :
        nextNode = frontier.pop() #extract from the start of the queue
        if problem.isGoalState(nextNode.state):
            return nextNode.solution()
        explored.add(nextNode.state)
        for successor, action, stepCost in problem.getSuccessors(nextNode.state):
            child = childNode(successor, nextNode, action, stepCost)
            if child.state not in explored:
                frontier.update(child, child.pathCost) #we only check if state is in explored because update does the other
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    class Node:
        def __init__(self, state, parent, action, pathCost):
            self.state = state
            self.parent = parent
            self.action = action
            self.pathCost = pathCost

        def solution(self):
          path = list()
          tempNode = self
          while tempNode.state != problem.getStartState():
              path.insert(0, tempNode.action)
              tempNode = tempNode.parent
          return path

        def __eq__(self, other):
            if isinstance(other, Node):
                return self.state == other.state


    def childNode(successor, parent, action, stepCost):
        pathCost = parent.pathCost + stepCost
        child = Node(successor, parent, action, pathCost)
        return child

    initialNode = Node(problem.getStartState(), None, None, 0)
    frontier = util.PriorityQueue() #bfs uses a queue
    frontier.push(initialNode, initialNode.pathCost + heuristic(initialNode.state, problem)) #we use f(n) = pathCost + h(n) for the best solution
    explored = set()

    while not frontier.isEmpty() :
        nextNode = frontier.pop() #extract from the start of the queue
        if problem.isGoalState(nextNode.state):
            return nextNode.solution()
        explored.add(nextNode.state)
        for successor, action, stepCost in problem.getSuccessors(nextNode.state):
            child = childNode(successor, nextNode, action, stepCost)
            if child.state not in explored:
                frontier.update(child, child.pathCost + heuristic(child.state, problem))
    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
