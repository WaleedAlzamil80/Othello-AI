import copy
import numpy as np
from Othello_Game import OthelloGame
from Nets import Polivy_model, Value_model

class MCTs_Node:
    def __init__(self, prior, state = None, to_play = 1, parent = None):
        self.prior = prior      # Prior probability for selecting this node given by the policy network
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

    def expand(self, state, to_play, action_props, game):
        self.state = state
        self.to_play = to_play

        for p, prop in enumerate(action_props):
            if prop != 0:
                action = (p // 8, p % 8)
                temp = copy.deepcopy(game)
                reward, done = temp.make_move(*action)
                self.children[action] = MCTs_Node(state = temp.board, prior = prop, to_play=-self.to_play, parent = self)
            
class MCTs:
    def __init__(self, game, num_simulations, model):
        self.game = copy.deepcopy(game)
        self.num_simulations = num_simulations
        self.model = model

    def simulation(self, value_net, policy_net, state = None, player = None):
        self.game.board.reset()
        if state != None and player != None:
            self.game.board.set_state(state, player)

        root = MCTs_Node(prior = 0, state = self.game.board, to_play=player)
        self._expand(root, value_net, policy_net, state, player)

        for i in range(self.num_simulations):
            node = root

            # Selection
            while node.IsExpaded():
                node, action = node.select_child()
                reward, done = self.game.make_move(*action)

            # Expansion and Simulation


            # Backprobagate
            self.backpropagate(node, reward)

        return node

    def _expand(self, node, value_net, policy_net, state, to_play):
        state_tensor = torch.tensor(state).type(torch.FloatTensor).reshape(1, -1)
        action_probs = policy_net.forward(state_tensor).reshape(-1).detach().cpu().numpy()
        value = value_net.forward(state_tensor).reshape(-1).detach().cpu().numpy()[0][0]
        valid_moves = self.game.get_valid_moves()
        action_prob_masked = np.zeros_like(action_probs)
        for row, col in valid_moves:
            action_prob_masked[0][row * 8 + col] = action_probs[0][row * 8 + col]
        action_probs /= np.sum(action_probs)
        temp_game = copy.deepcopy(self.game)
        node.expand(state, to_play, action_probs, temp_game)
        return value


    def backprobagate(self, node, reward):
        while node != None:
            node.visit_count += 1
            node.value_sum += reward
            reward *= -1
            node = node.parent