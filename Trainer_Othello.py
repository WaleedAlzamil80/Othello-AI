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
        current_state = self.game.board
        train_data = []

        while(True):
            pass

    def train(self, iterations = 10, epochs = 10):
        policy_losses = []
        value_losses = []
        for iter in range(iterations):
            train_data = []
            for eps in range(self.eps_per_iteration):
                train_data.extend(self.generate_episode())

            for epoch in range(epochs):
                self.policy_net.train()
                self.value_net.train()

                for batch in range(len(train_data) // self.batch_size):
                    continue