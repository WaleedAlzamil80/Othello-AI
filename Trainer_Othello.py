import torch
from torch import nn
import copy
import numpy as np
from Othello_Game import Othello_Game
from MCTs import MCTs
 

class MCTrainer:
    def __init__(self, environment, player, num_simulations, eps_per_iteration, batch_size):
        self.game = environment()
        self.MC = MCTs(board = copy.deepcopy(self.game), num_simulations = num_simulations)
        self.policy_net = nn.Sequential(nn.Linear(64, 128),
                                        nn.ReLU(),
                                        nn.Linear(128, 128),
                                        nn.ReLU(),
                                        nn.Linear(128, 64),
                                        nn.ReLU(),
                                        nn.Linear(64, 64),
                                        nn.Softmax(dim = 1)
                                        )
        self.value_net = nn.Sequential(nn.Linear(64, 128),
                                        nn.ReLU(),
                                        nn.Linear(128, 128),
                                        nn.ReLU(),
                                        nn.Linear(128, 64),
                                        nn.ReLU(),
                                        nn.Linear(64, 1),
                                        nn.Tanh()
                                        )
        self.player = player
        self.eps_per_iteration = eps_per_iteration
        self.batch_size = batch_size

        self.Voptim = torch.optim.Adam(self.value_net.parameters(), lr = 0.001)
        self.Poptim = torch.optim.Adam(self.policy_net.parameters(), lr = 0.001)
        self.Vloss = nn.MSELoss()
    
    def generate_episodes(self):
        self.game.reset()
        train_data = []

        while(True):
            tree = self.MC.simulation(self.Vpi, self.Ppi, self.game.board, self.game.current_player)
            action_probs = np.zeros(self.game.board.reshape(-1, 1).shape)
            for action, child in tree.children.items():
                action_probs[action[0] * 8 + action[1]] += child.visit_count

            valid_moves = self.game.get_valid_moves()
            for row, col in valid_moves:
                action_probs[row * 8 + col] = 0
            action_probs /= np.sum(action_probs)

            best_action = tree.select_action()
            train_data.append((self.game.board, self.game.current_player, action_probs))
            reward = self.game.make_move(best_action)
            if self.game.is_done():
                ret = []
                for state, player, action_prob in train_data:
                    ret.append((state, action_prob, reward * (-1) ** (player != self.game.current_player)))
                return ret


    def train(self, iterations = 10, epochs = 10):
        policy_losses = []
        value_losses = []
        policy_criterion = nn.CrossEntropyLoss()
        for iter in range(iterations):
            train_data = []
            for eps in range(self.eps_per_iteration):
                train_data.extend(self.generate_episode())

            for epoch in range(epochs):
                self.policy_net.train()
                self.value_net.train()

                for batch in range(len(train_data) // self.batch_size):
                    random_indeces = np.random.randint(len(train_data), size = self.batch_size)
                    states, policy_probs, values = list(zip(*[train_data[i] for i in random_indeces]))
                    states = torch.from_numpy(np.array(states)).type(torch.FloatTensor)
                    policy_probs = torch.from_numpy(np.array(states)).type(torch.FloatTensor)
                    values = torch.from_numpy(np.array(states)).type(torch.FloatTensor)

                    policy_pred = self.policy_net.forward(states)
                    value_pred = self.value_net.forward(states)

                    policy_loss = policy_criterion(policy_probs, values, policy_pred)
                    value_loss = torch.sum(torch.pow((values - value_pred), 2)) / values.shape[0]

                    self.Poptim.zero_grad()
                    policy_loss.backward()
                    self.Poptim.step()

                    self.Voptim.zero_grad()
                    value_loss.backward()
                    self.Voptim.step()

                policy_losses.append(float(policy_loss.detach().cpu()))
                value_losses.append(float(value_loss.detach().cpu()))

        self.policy_net.eval()
        self.value_net.eval()
        return policy_losses, value_losses