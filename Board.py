import numpy as np

class Board:
    def __init__(self):
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
    
    def is_valid_move(self, row, col):
        if self.board[row, col] != 0:
            return False
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self._is_valid_direction(row, col, dr, dc):
                    return True
        return False

    def _is_valid_direction(self, row, col, dr, dc):
        opponent = -self.current_player
        r, c = row + dr, col + dc
        if not (0 <= r < self.board_size and 0 <= c < self.board_size):
            return False

        if self.board[r, c] != opponent:
            return False

        r, c = r + dr, c + dc
        while 0 <= r < self.board_size and 0 <= c < self.board_size:
            if self.board[r, c] == 0:
                return False
            if self.board[r, c] == self.current_player:
                return True
            r, c = r + dr, c + dc
        return False

    def get_valid_moves(self):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            print("____InvalidMove_____")
            return
        self.board[row, col] = self.current_player
        self._flip_pieces(row, col)
        self.current_player *= -1
        ones = np.sum(self.board == 1)
        mones = np.sum(self.board == -1)

        if ones > mones:
            reward = 1
        elif mones > ones:
            reward = -1
        else:
            reward = 0

        return reward, self.is_done()
    
    def _flip_pieces(self, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self._is_valid_direction(row, col, dr, dc):
                    self._flip_direction(row, col, dr, dc)

    def _flip_direction(self, row, col, dr, dc):
        opponent = -self.current_player
        r, c = row + dr, col + dc
        while self.board[r, c] == opponent:
            self.board[r, c] = self.current_player
            r, c = r + dr, c + dc

    def is_done(self):
        # Check if game is over (no valid moves for either player)
        return False  # Placeholder
    
    def white_score(self):
        return str(np.sum(self.board == -1))
    
    def black_score(self):
        return str(np.sum(self.board == 1))
    
