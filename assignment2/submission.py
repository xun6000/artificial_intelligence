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
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument 
    is an object of GameState class. Following are a few of the helper methods that you 
    can use to query a GameState object to gather information about the present state 
    of Pac-Man, the ghosts and the maze.
    
    gameState.getLegalActions(): 
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action): 
        Returns the successor state after the specified agent takes the action. 
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    
    The GameState class is defined in pacman.py and you might want to look into that for 
    other helper methods, though you don't need to.
    
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    return successorGameState.getScore()


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
    Your minimax agent (problem 1)
    
    The auto grader will check the running time of your algorithm. Friendly reminder: passing the auto grader
    does not necessarily mean that your algorithm is correct.
  """

  
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following: 
      pacman won, pacman lost or there are no legal moves. 

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
	
      gameState.isWin():
        Returns True if it's a winning state
	
      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue
        
      It is recommended you have separate functions: value(), max_value(), and min_value() as in the slides
      and call these functions here to make your code understandable.
    """

    # BEGIN_YOUR_CODE (around 35 lines of code expected)
    # raise Exception("Not implemented yet")
    def Vopt(gameState,depth,idx):
      if idx == 0:
        depth = depth +1
      if gameState.isWin() or gameState.isLose() or depth>self.depth:
        score = self.evaluationFunction(gameState)
        return score, Directions.STOP

      next_idx = (idx+1)%gameState.getNumAgents()
      if idx == 0:
        acts = gameState.getLegalActions(idx)
        max_val = -float('Inf')
        max_act = None
        for act in acts:
          if act is Directions.STOP:
            continue
          next_state = gameState.generateSuccessor(idx, act)
          v, a = Vopt(next_state,depth,next_idx)
          if v > max_val:
            max_val = v
            max_act = act
        return max_val, max_act
      else:
        acts = gameState.getLegalActions(idx)
        min_val = float('Inf')
        min_act = None
        for act in acts:
          if act is Directions.STOP:
            continue
          next_state = gameState.generateSuccessor(idx, act)
          v, a = Vopt(next_state,depth,next_idx)
          if v < min_val:
            min_val = v
            min_act = act
        return min_val, min_act

    val, act = Vopt(gameState,0,self.index)
    print "value is ", val
    return act

    # END_YOUR_CODE

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
    
    The auto grader will check the running time of your algorithm. Friendly reminder: passing the auto grader
    does not necessarily mean your algorithm is correct.
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
      
      The same methods used in MinimaxAgent should also be useful here   
      
      It is recommended you have separate functions: value(), max_value(), and min_value() as in the slides
      and call these functions here to make the code clear   
    """

    # BEGIN_YOUR_CODE (around 45 lines of code expected)
    #raise Exception("Not implemented yet")
    def Vopt(gameState,depth,idx,alpha,beta):
      if idx == 0:
        depth+=1
      if gameState.isWin() or gameState.isLose() or depth>self.depth:
        score = self.evaluationFunction(gameState)
        return score, Directions.STOP

      next_idx = (idx+1)%gameState.getNumAgents()
      if idx == 0:
        acts = gameState.getLegalActions(idx)
        max_val = -float('Inf')
        max_act = None
        for act in acts:
          if act is Directions.STOP:
            continue
          next_state = gameState.generateSuccessor(idx, act)
          v, a = Vopt(next_state,depth,next_idx,alpha,beta)
          alpha = max(v,alpha)
          if alpha >= beta:
            return beta, a
          if v > max_val:
            max_val = v
            max_act = act
        return alpha, max_act
      else:
        acts = gameState.getLegalActions(idx)
        min_val = float('Inf')
        min_act = None
        for act in acts:
          if act is Directions.STOP:
            continue
          next_state = gameState.generateSuccessor(idx, act)
          v, a = Vopt(next_state,depth,next_idx,alpha,beta)
          beta = min(v,beta)
          if alpha >= beta:
            return alpha, a
          if v < min_val:
            min_val = v
            min_act = act
        return beta, min_act

    val, act = Vopt(gameState,0,self.index, -float('Inf'),float('Inf'))
    print "value is ", val
    return act
    # END_YOUR_CODE

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
    
    The auto grader will check the running time of your algorithm. Friendly reminder: passing the auto grader
    does not necessarily mean your algorithm is correct.
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
      
      The same methods used in MinimaxAgent should also be useful here   
      
      It is recommended you have separate functions: value(), max_value(), and expect_value() as in the slides
      and call these functions here to make the code clear
    """

    # BEGIN_YOUR_CODE (around 35 lines of code expected)
    # raise Exception("Not implemented yet")
    def Vopt(gameState,depth,idx):
      if idx == 0:
        depth=depth + 1
      if gameState.isWin() or gameState.isLose() or depth>self.depth:
        score = self.evaluationFunction(gameState)
        return score, Directions.STOP

      next_idx = (idx+1)%gameState.getNumAgents()
      if idx == 0:
        acts = gameState.getLegalActions(idx)
        max_val = -float('Inf')
        max_act = None
        for act in acts:
          if act is Directions.STOP:
            continue
          next_state = gameState.generateSuccessor(idx, act)
          v, a = Vopt(next_state,depth,next_idx)
          if v > max_val:
            max_val = v
            max_act = act
        return max_val, max_act
      else:
        acts = gameState.getLegalActions(idx)
        min_val = float('Inf')
        min_act = None
        act_num = 0
        min_sum = 0
        for act in acts:
          if act is Directions.STOP:
            continue
          act_num+=1
          next_state = gameState.generateSuccessor(idx, act)
          v, a = Vopt(next_state,depth,next_idx)
          min_sum+=v
          if v < min_val:
            min_val = v
            min_act = act
        return 1.0*min_sum/act_num, min_act

    val, act = Vopt(gameState,0,self.index)
    print "value is ", val
    return act
    # END_YOUR_CODE




def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
  """

  # BEGIN_YOUR_CODE (around 50 lines of code expected)
  # raise Exception("Not implemented yet")
  if currentGameState.isWin() or currentGameState.isLose():
    return currentGameState.getScore()
  food_distance = 0
  foodmap = currentGameState.getFood()
  paclocation = currentGameState.getPacmanPosition()
  
  
  for i in range(foodmap.width):
    for j in range(foodmap.height):
      if foodmap[i][j] == True: 
        # if food_distance > util.manhattanDistance((i,j),paclocation):
          food_distance += 1.0/util.manhattanDistance((i,j),paclocation)


  Capsules_list = currentGameState.getCapsules()
  capdistance = 0
  for caplocation in Capsules_list:
    # if capdistance > util.manhattanDistance(caplocation,paclocation):
      capdistance = capdistance + 1.0/util.manhattanDistance(caplocation,paclocation)


  gstate = currentGameState.getGhostStates()
  distanceofg, alertdistance , quickly_run= 0, 0, False
  
  for idx,g in enumerate(gstate):
    if g.scaredTimer == 0:
      #if distanceofg > util.manhattanDistance(paclocation,currentGameState.getGhostPosition(idx+1)):
      temp = util.manhattanDistance(paclocation,currentGameState.getGhostPosition(idx+1))
      if temp > 10:
        distanceofg+=10
      else:
        if temp < 3:
          quickly_run = True
        distanceofg=temp +distanceofg
    else:
      alertdistance = alertdistance + 1.0/util.manhattanDistance(paclocation,currentGameState.getGhostPosition(idx+1))

  if quickly_run:
    return currentGameState.getScore() + 3*food_distance + 5*distanceofg + 5*capdistance + 2*alertdistance
  else:
    return currentGameState.getScore() + 3*food_distance + distanceofg + 2*alertdistance
  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction


