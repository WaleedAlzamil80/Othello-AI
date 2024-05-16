import copy 
import numpy as np

class OthelloGAME:
    def __init__(self, rules):
        self.rules = rules
        self.board_size = 8
        self.board = np.zeros((self.board_size, self.board_size), dtype=int) # 1: player1, -1: player2,  0: Empty
        self.board[3, 3] = self.board[4, 4] = 1
        self.board[3, 4] = self.board[4, 3] = -1
        self.current_player = 1
        self.reset()

    def reset(self):
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = -1
        self.current_player = 1

    def set_state(self, state, to_play):
        self.board = self.rules.initial_state()
        self.current_player = to_play

    def get_valid_moves(self):
        return self.rules.get_valid_moves(self.board, self.current_player)

    def make_move(self, row, col):
        self.board, _, _ = self.rules.make_move(self.board, self.current_player, row, col)
        self.current_player *= -1

    def white_score(self):
        return np.sum(self.board == -1)

    def black_score(self):
        return np.sum(self.board == 1)

    def is_done(self):
        v1 = self.get_valid_moves()
        self.current_player *= -1
        v2 = self.get_valid_moves()
        self.current_player *= -1
        return ((len(v1) == 0) and (len(v2) == 0))

    def MinMax_vs_MCTs(self, depth = 3, alpha_beta = False, mcts = None):
        while not self.is_done():
            print("Current board:")
            print(self.board)
            print("Player", self.current_player, "to move.")
            if self.current_player == 1:
                valid_moves = self.get_valid_moves()
                print("Valid moves:", valid_moves)
                mcts_probs = mcts.search(self.board, self.current_player)
                action = np.argmax(mcts_probs)
                row = action // 8
                col = action % 8
                print("MCTs-move: ", row, col)
                if (row, col) in valid_moves:
                        print("MCTs playes")
                        self.make_move(row, col)
                else:
                        print("Invalid move. Try again.")
            else:
                print("AI is thinking...")
                valid_moves = self.get_valid_moves()
                if valid_moves:
                    print("Valid moves:", valid_moves)

                row, col = self.get_best_move(depth=depth, alpha_beta = alpha_beta)
                print("MiMa-move: ", row, col)
                self.make_move(row, col)

        ones = np.sum(self.board == 1)
        mones = np.sum(self.board == -1)
        print("-----------------------WINNNNNER-----------------------------")
        print("Player 1: ", ones)
        print("Player -1: ", mones)