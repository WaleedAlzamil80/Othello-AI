from MCTs.MCTs import *
from MCTs.OthelloGame_for_MCTs import *
from Othello_Game import *


othello = OthelloGame()
game = OthelloGAME()
mcts = MCTs(othello, 1000)

while not game.is_done():
      state = copy.deepcopy(game.board)
      print("Current board:")
      ones = np.sum(game.board== 1)
      mones = np.sum(game.board == -1)
      print("Player 1: ", ones)
      print("Player -1: ", mones)
      print(state)
      print("------------------------------------------------------")

      valid_moves = game.get_valid_moves()
      if not valid_moves:
          print("No valid moves. Skipping turn.")
          game.current_player *= -1
          continue
      print("Valid moves: ", valid_moves)
      if game.current_player == 1:
          print("MiMa player: ", game.current_player)

          row, col = game.get_best_move(depth=2, alpha_beta = True)
          print(row, col)
          game.make_move(row, col)
      else:
          print("MCTs player: ", game.current_player)
          mcts_probs = mcts.search(state, game.current_player)
          action = np.argmax(mcts_probs)
          row = action // 8
          col = action % 8
          print(row, col)
          game.make_move(row, col)