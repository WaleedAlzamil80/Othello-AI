import copy
import numpy as np
from Othello_Game import Othello_Game

class MCTs_Node:
    def __init__(self, state = None, to_play = 1, parent = None):
        self.state = state      # Board
        self.player = to_play   # Player that need to take the action
        self.parent = parent    # The state's parent node in tree
        self.visit_count = 0    # The number of times this node has been visited by MCTs
        self.win_count = 0      # The number of times this node result to win the player to play
        self.values_sum = 0     # The sum of the environment heuristic of this state through running MCTs
        self.children = {}      # look up table - action : child (state: board)

    def IsExpaded(self):
        return len(self.children) > 0

    def nodeValue(self):
        return self.values_sum / (self.visit_count + 1e-6)

    def randomAction(self):
        actions = [action for action in self.children.keys()]
        return np.random.choice(actions)

    def select_action(self, ucb = True):
        visit_counts = np.array([child.visit_count for child in self.children.values()])
        actions = np.array([child.visit_count for child in self.children.keys()])
        if ucb:
            return actions[np.argmax(visit_counts)]
        return actions[np.argmax([child.nodeValue for child in self.children.values()])]

    def select_child(self):
        bestScore = -np.inf
        bestChild = None
        bestAction = -1

        ########### Selection ###########
        for action, child in self.actions.items():
            score = self.calcUCB(child)
            if score > bestScore:
                bestScore, bestChild, bestAction = score, child, action
        return bestChild, bestAction

    def calcUCB(self, child):
        return child.nodeValue() - np.sqrt(2 * np.log(self.visited) / (child.visited + 1))

    def expand(self, state, to_play, action_props):
        self.state = state
        self.to_play = to_play

        for p, prop in enumerate(action_props):
            if prop > 1e-7:
                self.children[p] = MCTs_Node()

    def simulate(self, game, depth):
        """Simulate from this node and update the value of each nodes"""
        current = self
        while depth != 0:
            action = current.select_action()
            nextState = game.getNextState(current.state, action)
            if game.isEndOfGame(nextState):
                reward = game.getReward(nextState, -current.player)
                while current is not None:
                    current.values_sum += reward * current.nodeValue()
                    current.visit_count += 1
                    current = current.parent
                break
            else:
                current = current.children[action]
                depth -= 1
class MCTs:
    def __init__(self, board, num_simulations, game):
        self.board = board
        self.num_simulations = num_simulations
        self.game = game
        self.root = MCTs_Node(copy.deepcopy(game.board))

    def simulation(self, Vpi, Ppi, state, player):
        pass