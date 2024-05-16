import numpy as np

class Board:
    def __init__(self, rules):
        self.rules = rules
        self.board_size = 8
        self.board = np.zeros((self.board_size, self.board_size), dtype=int) # 1: player1, -1: player2,  0: Empty
        self.board[3, 3] = self.board[4, 4] = 1
        self.board[3, 4] = self.board[4, 3] = -1
        self.current_players = 1
        self.reset()

    def reset(self):
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = -1
        self.current_player = 1

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
