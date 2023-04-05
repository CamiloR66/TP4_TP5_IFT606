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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        ============================================================
        QUESTION 1

        Vous devez compléter cette méthode afin d'améliorer l'évaluation de l'action
        donnée en paramètre par rapport à l'état actuel (donné en paramètre également).

        GameState.getScore() retourne simplement le score prévu à l'état, le score affiché
        dans l'interface.
        ============================================================

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
        pos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newCapsules = successorGameState.getCapsules()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        # Score initial
        score = 0.0

        # Regarder les conditions de fin de la partie
        if successorGameState.isLose():
            return -1000.0
        if successorGameState.isWin():
            return 1000.0
        
        # Pour favoriser les déplacements
        if pos == newPos:
            score -= 10.0

        # Trouver la capsule la plus proche
        bestCapsule = None
        minCapsuleDist = float("inf")
        for capsule in newCapsules:
            capsuleDistance = manhattanDistance(newPos, capsule)
            if capsuleDistance < minCapsuleDist:
                bestCapsule = capsule
                minCapsuleDist = capsuleDistance

        # Trouver la food la plus proche
        bestFood = None
        minFoodDist = float("inf")
        for food in newFood:
            foodDistance = manhattanDistance(newPos, food)
            if foodDistance < minFoodDist:
                bestFood = food
                minFoodDist = foodDistance

        # Augmenter le score si Pacman mange
        if minCapsuleDist == 0.0:
            score += 10.0
        elif minFoodDist == 0.0:
            score += 5.0
        
        # Diminuer le score si Pacman s'éloigne des objectifs
        elif minCapsuleDist == minFoodDist or minCapsuleDist < minFoodDist:
            if manhattanDistance(pos, bestCapsule) < minCapsuleDist: 
                score -= 10.0
        else:
            if manhattanDistance(pos, bestFood) < minFoodDist: 
                score -= 5.0

        # Ajuster le score selon l'état et la distance des fantômes
        for i in range(len(newGhostStates)):
            ghostDistance = manhattanDistance(newPos, newGhostStates[i].getPosition())
            # Si les fantômes sont effrayés, favoriser l'approche
            if newScaredTimes[i] > 0.0:
                if ghostDistance == 0.0:
                    score += 100.0
                else:
                    score += 1.0 / ghostDistance
            # Si les fantômes ne sont pas effrayés, favoriser la distance
            else:
                score -= 10.0 / ghostDistance

        return score


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

    def getAction(self, gameState):
        """
        ============================================================
        QUESTION 2

        Vous devez compléter cette méthode afin d'implémenter le choix de l'action selon
        l'algorithme minimax.

        Puisqu'il vous est demandé d'arrêter la recherche à une profondeur maximale donnée (self.depth),
        vous devez utiliser la fonction d'évaluation de l'agent self.evaluationFunction().
        ============================================================

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minmax(state, depth, agentIndex):
            # Si c'est un noeud terminal, retourner la valeur
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            
            # Si c'est un noeud Pacman
            if agentIndex == 0:
                bestScore = float("-inf")
                bestAction = None
                # Trouver l'action qui maximise l'utilité
                for action in state.getLegalActions(0):
                    newGameState = state.generateSuccessor(0, action)
                    score, _ = minmax(newGameState, depth, 1)
                    if score > bestScore:
                        bestScore = score
                        bestAction = action
                return bestScore, bestAction
            
            # Sinon c'est un fantôme
            else:
                bestScore = float("inf")
                bestAction = None
                # Trouver l'action qui minimise l'utilité
                for action in state.getLegalActions(agentIndex):
                    newGameState = state.generateSuccessor(agentIndex, action)
                    if agentIndex == state.getNumAgents() - 1:
                        score, _ = minmax(newGameState, depth - 1, 0)
                    else:
                        score, _ = minmax(newGameState, depth, agentIndex + 1)
                    if score < bestScore:
                        bestScore = score
                        bestAction = action
                return bestScore, bestAction    

        _, action = minmax(gameState, self.depth, 0)
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        ============================================================
        QUESTION 3

        Vous devez compléter cette méthode afin d'implémenter le choix de l'action selon
        l'algorithme alpha-beta pruning.
        ============================================================

        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(state, depth, agentIndex, alpha, beta):
            # Si c'est un noeud terminal, retourner la valeur
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            
            # Si c'est un noeud Pacman
            if agentIndex == 0:
                # Trouver l'action qui maximise l'utilité
                bestScore = float("-inf")
                bestAction = None
                for action in state.getLegalActions(0):
                    newGameState = state.generateSuccessor(0, action)
                    score, _ = alphabeta(newGameState, depth, 1, alpha, beta)
                    if score > bestScore:
                        bestScore = score
                        bestAction = action
                    if bestScore > beta:
                        return bestScore, action

                    alpha = max(alpha, bestScore)
                return bestScore, bestAction
            
            # Sinon, c'est un noeud fantôme
            else:
                bestScore = float("inf")
                bestAction = None
                # Trouver l'action qui minimise l'utilité
                for action in state.getLegalActions(agentIndex):
                    newGameState = state.generateSuccessor(agentIndex, action)
                    if agentIndex == state.getNumAgents() - 1:
                        score, _ = alphabeta(newGameState, depth - 1, 0, alpha, beta)
                    else:
                        score, _ = alphabeta(newGameState, depth, agentIndex + 1, alpha, beta)
                    if score < bestScore:
                        bestScore = score
                        bestAction = action
                    if bestScore < alpha:
                        return bestScore, bestAction

                    beta = min(beta, bestScore)
                return bestScore, bestAction    

        _, action = alphabeta(gameState, self.depth, 0, float("-inf"), float("inf"))
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        ============================================================
        QUESTION 4

        Vous devez compléter cette méthode afin d'implémenter le choix de l'action selon
        l'algorithme expectimax.
        ============================================================

        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiminmax(state, depth, agentIndex):
            # Si c'est un état terminal, retourner la valeur
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            
            # Si c'est un noeud chance, calculer la somme des utilités selon une probabilité uniforme
            if agentIndex != 0:
                totalScore = 0
                actions = state.getLegalActions(agentIndex)
                # Calculer la moyenne des scores pour chaque action
                for action in actions:
                    newGameState = state.generateSuccessor(agentIndex, action)
                    prob = 1.0 / len(actions)
                    # Si c'est le dernier noeud fantôme, le prochain noeud est Pacman
                    if agentIndex == state.getNumAgents() - 1:
                        score, _ = expectiminmax(newGameState, depth - 1, 0)
                    # Sinon, c'est un autre noeud fantôme
                    else:
                        score, _ = expectiminmax(newGameState, depth, agentIndex + 1)
                    # Ajouter le score en fonction de la probabilit,
                    totalScore += prob * score
                return totalScore, None
            
            # Sinon, c'est un noeud Pacman
            else:
                # Trouver l'action qui maximise l'utilité
                bestScore = float("-inf")
                bestAction = None
                for action in state.getLegalActions(0):
                    newGameState = state.generateSuccessor(0, action)
                    score, _ = expectiminmax(newGameState, depth, 1)
                    if score > bestScore:
                        bestScore = score
                        bestAction = action
                return bestScore, bestAction

        _, action = expectiminmax(gameState, self.depth, 0)
        return action

def betterEvaluationFunction(currentGameState):
    """
    ============================================================
    QUESTION 5

    Vous devez compléter cette méthode afin d'évaluer l'état donné en
    paramètre.
    ============================================================

    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    """

    "*** VOTRE EXPLICATION ICI ***"
    """
    La fonction d'évalutation calcul la valeur de l'état en fonction de trois critères :
     - Les fantômes
     - La capsule la plus proche
     - La nourriture la plus proche
    Pacman suit les priorités suivantes : 
     - Manger un fantôme effrayé s'il est plus près que la nourriture
     - S'éloigner des fantômes plus ils sont près
     - Manger une capsule si elle est plus près que la nourriture
     - Manger de la nourriture si elle est plus proche qu'une capsule

    La fonction ne fait qu'un seul niveau de l'arbre, l'état courant, autrement l'algorithme finissait toujours en timeout.

    Pour simplifier l'algorithme on ne tient pas compte des murs ou de la quantité de nourriture, seulement la plus proche.
    """
    "*** YOUR CODE HERE ***"
    # Variables de l'état du jeu
    pos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newCapsules = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Score initial
    score = 0.0

    # Regarder les conditions de fin de la partie
    if currentGameState.isLose():
        return -1000.0
    if currentGameState.isWin():
        return 1000.0

    # Trouver la capsule la plus proche
    minCapsuleDist = float("inf")
    for capsule in newCapsules:
        capsuleDistance = manhattanDistance(pos, capsule)
        if capsuleDistance < minCapsuleDist:
            minCapsuleDist = capsuleDistance

    # Trouver la nourriture la plus proche
    minFoodDist = float("inf")
    for food in newFood:
        foodDistance = manhattanDistance(pos, food)
        if foodDistance < minFoodDist:
            minFoodDist = foodDistance

    # Augmenter le score si Pacman mange
    if minCapsuleDist == 0.0:
        score += 20.0
    elif minFoodDist == 0.0:
        score += 5.0
    
    # Ajuster le score selon l'état et la distance des fantômes
    for i in range(len(newGhostStates)):
        ghostDistance = manhattanDistance(pos, newGhostStates[i].getPosition())
        # Si les fantômes sont effrayés, favoriser l'approche
        if newScaredTimes[i] > 0.0:
            if ghostDistance == 0.0:
                score += 100.0
            else:
                if minFoodDist + 2.0 < ghostDistance:
                    score -= 1.0 / ghostDistance
                elif minFoodDist + 4.0 < ghostDistance:
                    score -= 10.0 / ghostDistance
                else:
                    score += 1.0 / ghostDistance
        # Si les fantômes ne sont pas effrayés, favoriser la distance
        else:
            score -= 10.0 / ghostDistance

    return score

# Abbreviation
better = betterEvaluationFunction
