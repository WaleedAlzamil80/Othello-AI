import copy
import numpy as np
from MCTs_Actor_Critic import *
from OthelloGame import *
from Othello_Game import *
from Nets import *
from RL import *

othello = OthelloGame()
game = OthelloGAME()
model = ResNet(othello, 4, 64)
mcts = MCTs_RL(othello, 100, model)

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
model = ResNet(othello, 4, 64)
mcts = MCTs_RL(othello, 1000, model)
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001)

LaylaZero = AlphaZero(GAME = othello, model = model, optimizer = optimizer)
poly, valy = LaylaZero.learn()