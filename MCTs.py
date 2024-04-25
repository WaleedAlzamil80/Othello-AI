import tqdm
import copy
import numpy as np
from Othello_Game import Othello_Game

class MCTs_Node:
    def __init__(self, prior, state = None, to_play = 1, parent = None):
        self.pripr = prior      # Prior probability for selecting this node given by the policy network
        self.state = state      # Board
        self.player = to_play   # Player that need to take the action
        self.parent = parent    # The state's parent node in tree
        self.visit_count = 0    # The number of times this node has been visited by MCTs
        self.values_sum = 0     # The sum of the environment heuristic of this state through running MCTs
        self.children = {}      # look up table - action : child (MCTs_Node)

    def IsExpaded(self):
        return len(self.children) > 0

    def nodeValue(self):
        if self.visit_count == 0:
            return 0
        return self.values_sum / self.visit_count

    def select_action(self):
        actions = [action for action in self.children.keys()]
        return actions[np.argmax([child.visit_count for child in self.children.values()])]

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
        prior_score = child.prior * np.sqrt(self.visit_count) / (child.visit_count + 1)
        if child.visit_count > 0:
            value_score = -child.nodeValue()
        else:
            value_score = 0
        return value_score + prior_score

    def expand(self, state, to_play, action_props):
        self.state = state
        self.to_play = to_play

        for p, prop in enumerate(action_props):
            if prop != 0:
                self.children[p] = MCTs_Node(prior = prop, to_play=-self.to_play, parent = self)

class MCTs:
    def __init__(self, game, num_simulations, model):
        self.game = copy.deepcopy(game)
        self.num_simulations = num_simulations
        self.model = model

    def simulation(self, Vpi, Ppi, state = None, player = None):
        if state != None and player != None:
            self.game.board.reset()
            self.game.board.set_state(state, player)

        root = MCTs_Node(0, state = self.game.board, to_play=player)
        self._expand(root, Vpi, Ppi, state, player)

        for i in range(self.num_simulations):
            node = root

            # Selection
            while node.IsExpaded():
                node, action = node.select_child()
                reward = self.game.make_move(action)

            # Expansion
            state = self.game.board
            self.game.make_move(action)

            if not self.game.is_done():
                reward = self._expand()

            # backprobagation
            self.backpropagate(node, reward)

        return node

    def  _expand(self, node, Vpi, Ppi, state, player):
        node.Expand(Vpi, Ppi, state, player)

    def backpropagate(self, node, reward):
        while node != None:
            node.visit_count += 1
            node.value_sum += reward
            reward *= -1
            node = node.parent

# value = child_node.win_count / child_node.visit_count + exploration_param * np.sqrt(np.log(node.visit_count) / child_node.visit_count)