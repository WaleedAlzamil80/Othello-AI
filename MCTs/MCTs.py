import copy
import numpy as np

class MCTs_Node:
    def __init__(self, game, to_play = 1, state = None, parent = None, action_taken = None):
        self.state = state      # Board
        self.player = to_play   # Player that need to take the action
        self.parent = parent    # The state's parent node in tree
        self.visit_count = 0    # The number of times this node has been visited by MCTs
        self.values_sum = 0     # The sum of the environment heuristic of this state through running MCTs
        self.children = []
        self.game = game
        self.expandable_moves = self.game.get_valid_moves(state, to_play)

    def IsExpaded(self):
        return len(self.children) > 0

    def IsFullExpanded(self):
        return len(self.expandable_moves) == 0

    def nodeValue(self):
        if self.visit_count == 0:
            return 0
        return self.values_sum / self.visit_count

    def select_child(self):
        bestScore = -np.inf
        bestChild = None
        bestAction = -1

        ########### Selection ###########
        for child in self.children:
            score = self.calcUCB(child)
            if score > bestScore:
                bestScore, bestChild = score, child
        return bestChild

    def calcUCB(self, child):
        prior_score = child.prior * np.sqrt(self.visit_count) / (child.visit_count + 1)
        if child.visit_count > 0:
            value_score = -child.nodeValue()
        else:
            value_score = 0
        return value_score + prior_score

    def expand(self):
        action = np.random.choice(self.expandable_moves)
        self.expandabel_moves.remove(action)
        child_state = copy.deepcopy(self.state)
        child_state, _, _ = self.game.make_move(child_state, action, self.player)
        self.children.append(MCTs_Node(self.game, -self.player, child_state, self, action))
        return self.children[-1]

    def simulation(self):
        value, is_ternminal = self.game.value_termination(self.state)
        if is_terminal:
          return value

        rollout_state = copy.deepcopy(self.state)
        rollout_player = self.player
        while True:
          valid_moves = self.game.get_valid_moves(rollout_state)
          action = np.random.choice(valid_moves)
          rollout_state, _, _ = self.game.make_move(rollout_state, action, rollout_player)
          value, is_terminal = self.game.value_termination(rollout_state)
          if is_terminal:
              return value
          rollout_player *= -1          


class MCTs:
    def __init__(self, game, num_simulations):
        self.game = copy.deepcopy(game)
        self.num_simulations = num_simulations

    def search(self, state = None, player = None):

        root = MCTs_Node(self.game, state = state, to_play=player)

        for i in range(self.num_simulations):
            node = root

            # Selection
            while node.IsFullExpanded():
                node = node.select_child()

            value, is_terminal = self.game.value_termination(node.state)

            # Expansion and Simulation
            if not is_terminal:
                node = node.expand()
                value = node.simulate()

            # Backprobagate
            self.backprobagate(node, value)

        action_probs = np.zeros(self.game.action_space)
        for child in root.children:
            row, col = child.take_action[0], child.take_action[1]
            action_probs[row * 8 + col] = child.visit_count
        action_probs /= np.sum(action_probs)

        return action_probs

    def backprobagate(self, node, value):
        while node != None:
            node.visit_count += 1
            node.values_sum += value
            value *= -1
            node = node.parent