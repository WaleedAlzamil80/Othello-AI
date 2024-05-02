import copy
import numpy as np
import argparse

from RL.MCTs_Actor_Critic import *
from RL.OthelloGame import *
from Othello_Game import *
from RL.Nets import *
from RL.RL import *

parser = argparse.ArgumentParser(description="Specify the algorithms parameters.")

# Arguments for inference and play
parser.add_argument("--search", type=int, default=1000, help="Searching and exploring the Game Space (Simulation)")
parser.add_argument("--NH", type=int, default=64, help="Number of hidden layers")
parser.add_argument("--NB", type=int, default=4, help="Number of residual blocks")

# Arguments used just during training
parser.add_argument("--BatchSize", type=int, default=64, help="Batch Size")
parser.add_argument("--epochs", type=int, default=5, help="Epochs")
parser.add_argument("--self_play", type=int, default=500, help="Number of Games the model play before training")
parser.add_argument("--iterations", type=int, default=5, help="Number of iteration the model play against  itself before training")
parser.add_argument("--lr", type=float, default=0.001, help="Learning rate used while training")

args = parser.parse_args()

othello = OthelloGame()
game = OthelloGAME()
model = ResNet(othello, args.NB, args.BatchSize)
mcts = MCTs_RL(othello, args.search, model)

while not game.is_done():
      state = copy.deepcopy(game.board)
      ones = np.sum(game.board== 1)
      mones = np.sum(game.board == -1)
      valid_moves = game.get_valid_moves()

      print("Current board:")
      print("Player 1: ", ones)
      print("Player -1: ", mones)
      print(state)
      print("------------------------------------------------------")

      if not valid_moves:
          print("No valid moves. Skipping turn.")
          game.current_player *= -1
          continue
      print("Valid moves: ", valid_moves)
      if game.current_player == 1:
          print("MiMa player: ", game.current_player)

          row, col = game.get_best_move(depth=1, alpha_beta = True)
          print(row, col)
          game.make_move(row, col)
      else:
          print("MCTs player: ", game.current_player)
          state = copy.deepcopy(game.board)
          mcts_probs = mcts.search(state, game.current_player)
          action = np.argmax(mcts_probs)
          row = action // 8
          col = action % 8
          print(row, col)
          game.make_move(row, col)


othello = OthelloGame()
game = OthelloGAME()
model = ResNet(othello, args.NB, args.BatchSize)
mcts = MCTs_RL(othello, args.search, model)

optimizer = torch.optim.Adam(model.parameters(), lr = args.lr)

LaylaZero = AlphaZero(GAME = othello, model = model, optimizer = optimizer, num_iteration = args.iterations, play_iteration = args.self_play, epochs = args.epochs, batch_size = args.batchSize, num_simulation = args.search)
poly, valy = LaylaZero.learn()