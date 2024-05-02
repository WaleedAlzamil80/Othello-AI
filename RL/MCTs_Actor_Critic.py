import copy
import numpy as np
import torch

class MCTs_Node_RL:
    def __init__(self, game, to_play = 1, state = None, parent = None, action_taken = None, prior = None):
        self.prior = prior
        self.action_taken = action_taken
        self.state = state      # Board
        self.player = to_play   # Player that need to take the action
        self.parent = parent    # The state's parent node in tree
        self.visit_count = 0    # The number of times this node has been visited by MCTs
        self.values_sum = 0     # The sum of the environment heuristic of this state through running MCTs
        self.children = []
        self.game = game

    def IsExpanded(self):
        return len(self.children) > 0

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
        prior_score = np.sqrt(self.visit_count) / (child.visit_count + 1)
        if child.visit_count > 0:
            q_value = 1 - (child.values_sum / (child.visit_count + 1)) / 2
        else:
            q_value = 0
        return q_value + child.prior * 2 * np.sqrt(np.log(self.visit_count)) / (child.visit_count + 1)

    def expand(self, policy):
        for ind, prob in enumerate(policy):
            if prob > 0:
              child_state = copy.deepcopy(self.state)
              child_state, _, _ = self.game.make_move(child_state, self.player, ind // 8, ind % 8)
              self.children.append(MCTs_Node_RL(self.game, -self.player, child_state, self, ind, prob))

        return self.children[-1]

class MCTs_RL:
    def __init__(self, game, num_simulations, model):
        self.game = copy.deepcopy(game)
        self.num_simulations = num_simulations
        self.model = model

    def search(self, state = None, player = None):

        root = MCTs_Node_RL(self.game, state = state, to_play=player)

        for i in range(self.num_simulations):
            node = root

            # Selection
            while node.IsExpanded():
                node = node.select_child()

            value, is_terminal = self.game.value_termination(node.state)

            # Expansion and Simulation
            valid_moves = self.game.get_valid_moves(node.state, node.player)
            if (len(valid_moves) > 0) and (not is_terminal):
                policy, value = self.model.predict(torch.tensor(self.game.encoded_state(node.state)).reshape(-1, 3, 8, 8))
                valid_moves = self.game.get_valid_moves(node.state, node.player)
                policy = policy.detach().cpu().numpy().reshape(-1)
                value = value.detach().cpu().numpy()[0][0]
                mask = np.zeros_like(policy)
                for move in valid_moves:
                    mask[move[0] * 8 + move[1]] = 1
                policy *= mask

                # print(policy, valid_moves)
                policy /= np.sum(policy)
                node = node.expand(policy)

            # Backprobagate
            self.backprobagate(node, value)

        action_probs = np.zeros(self.game.action_space)
        for child in root.children:
            row, col = child.action_taken // 8, child.action_taken % 8
            action_probs[row * 8 + col] = child.visit_count
        action_probs /= np.sum(action_probs)

        return action_probs

    def backprobagate(self, node, value):
        while node != None:
            node.visit_count += 1
            node.values_sum += value
            value *= -1
            node = node.parent