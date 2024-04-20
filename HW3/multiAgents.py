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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
        First, we get the legal actions for pacman. Then, we iterate over all the actions and get
        the score for each action. If the agent is pacman, we get the maximum score, otherwise we
        get the minimum score. We return the action with the maximum score. When we reach the depth
        limit or the game is over, we return the evaluation function.
        """
        actions = gameState.getLegalActions(0) # get legal actions for pacman
        candidates = [] # list of (score, action) tuples
        for action in actions:
            candidate = self.minimax(gameState.getNextState(0, action), self.depth-1, 1)
            candidates.append((candidate, action))
        # print(candidates)
        return max(candidates)[1]
    
    def minimax(self, gameState, depth, agentIndex):
        if (depth == 0 and agentIndex == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex)
        candidates = []
        if agentIndex == 0:
            for action in actions:
                candidate = self.minimax(gameState.getNextState(agentIndex, action), depth-1, 1)
                candidates.append(candidate)
            return max(candidates)
        elif agentIndex >= 1 and agentIndex < gameState.getNumAgents()-1:
            for action in actions:
                candidate = self.minimax(gameState.getNextState(agentIndex, action), depth, agentIndex+1)
                candidates.append(candidate)
            return min(candidates)
        else: # agentIndex == gameState.getNumAgents()-1
            for action in actions:
                candidate = self.minimax(gameState.getNextState(agentIndex, action), depth, 0)
                candidates.append(candidate)
            return min(candidates) 
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        First, we get the legal actions for pacman. Then, we iterate over all the actions and get 
        the score for each action. If the agent is pacman, we get the maximum score, otherwise we 
        get the minimum score. We return the action with the maximum score. When we reach the depth
        limit or the game is over, we return the evaluation function. We use alpha-beta pruning to 
        reduce the number of nodes we need to explore.
        """
        actions = gameState.getLegalActions(0)
        candidates = []
        alpha = float('-inf')
        beta = float('inf')
        for action in actions:
            candidate = self.alphaBeta(gameState.getNextState(0, action), self.depth-1, 1, alpha, beta)
            candidates.append((candidate, action))
            alpha = max(alpha, candidate)
        # print(candidates)
        return max(candidates)[1]
    
    def alphaBeta(self, gameState, depth, agentIndex, alpha, beta):
        if (depth == 0 and agentIndex == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            v = float('-inf')
            for action in actions:
                v = max(v, self.alphaBeta(gameState.getNextState(agentIndex, action), depth-1, 1, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v
        elif agentIndex >= 1 and agentIndex < gameState.getNumAgents()-1:
            v = float('inf')
            for action in actions:
                v = min(v, self.alphaBeta(gameState.getNextState(agentIndex, action), depth, agentIndex+1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        else:
            v = float('inf')
            for action in actions:
                v = min(v, self.alphaBeta(gameState.getNextState(agentIndex, action), depth, 0, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        First, we get the legal actions for pacman. Then, we iterate over all the actions and get 
        the score for each action. If the agent is pacman, we get the maximum score, otherwise we 
        get the average score. We return the action with the maximum score. When we reach the depth
        limit or the game is over, we return the evaluation function. We use expectimax to model 
        the ghosts as choosing uniformly at random from their legal moves.
        """
        actions = gameState.getLegalActions(0)
        candidates = []
        for action in actions:
            candidate = self.expectimax(gameState.getNextState(0, action), self.depth-1, 1)
            candidates.append((candidate, action))
        # print(candidates)
        return max(candidates)[1]
    
    def expectimax(self, gameState, depth, agentIndex):
        if (depth == 0 and agentIndex == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            candidates = []
            for action in actions:
                candidate = self.expectimax(gameState.getNextState(agentIndex, action), depth-1, 1)
                candidates.append(candidate)
            return max(candidates)
        elif agentIndex >= 1 and agentIndex < gameState.getNumAgents()-1:
            candidates = []
            for action in actions:
                candidate = self.expectimax(gameState.getNextState(agentIndex, action), depth, agentIndex+1)
                candidates.append(candidate)
            return sum(candidates) / len(candidates) # average of all ghost actions
        else:
            candidates = []
            for action in actions:
                candidate = self.expectimax(gameState.getNextState(agentIndex, action), depth, 0)
                candidates.append(candidate)
            return sum(candidates) / len(candidates) # average of all ghost actions
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    We calculate the score based on the following factors:
    1. If the game is won, return infinity, while if the game is lost, return negative infinity.
    2. If the ghost is within 1 unit of pacman, return negative infinity to avoid getting caught.
    3. If the ghost is scared, add 10 times the scared time to the score to encourage pacman to eat
       the ghost.
    4. If the average distance to food is less, add 10 divided by the average distance to food to 
       the score to encourage pacman to eat the food.
    5. If the minimum distance to the ghost is less, add 20 divided by the minimum distance to the 
       ghost to the score to avoid getting caught.
    6. Subtract 5 times the number of food left and 10 times the number of capsules left to 
       encourage pacman to eat the food and capsules.
    """
    if currentGameState.isWin():
        return float('inf')
    if currentGameState.isLose():
        return float('-inf')
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    minGhostDistance = min([manhattanDistance(pos, state.getPosition()) for state in ghostStates])
    avgFoodDistance = sum([manhattanDistance(pos, food) for food in food.asList()])/(len(food.asList())+1)
    score = currentGameState.getScore()
    
    if minGhostDistance <= 1:
        return float('-inf')
    score += 10*scaredTimes[0]
    score += 10.0/(avgFoodDistance+1)
    score += 20.0/(minGhostDistance+1)
    score -= 5*len(food.asList())
    score -= 10*len(capsules)
    return score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
