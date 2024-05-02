import numpy as np

class OthelloGame:
    def init(self):
        self.board_size = 8
        self.action_space = self.board_size ** 2

    def initial_state(self):
        state = np.zeros((self.board_size, self.board_size), dtype=int) # 1: player1, -1: player2,  0: Empty
        state[3][3] = state[4][4] = 1
        state[3][4] = state[4][3] = -1
        return state

    def is_valid_move(self, state, player, row, col):
        if state[row, col] != 0:
            return False
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self._is_valid_direction(state, player, row, col, dr, dc):
                    return True
        return False

    def _is_valid_direction(self, state, player, row, col, dr, dc):
        opponent = -player
        r, c = row + dr, col + dc
        if not (0 <= r < self.board_size and 0 <= c < self.board_size):
            return False

        if state[r, c] != opponent:
            return False

        r, c = r + dr, c + dc
        while 0 <= r < self.board_size and 0 <= c < self.board_size:
            if state[r, c] == 0:
                return False
            if state[r, c] == player:
                return True
            r, c = r + dr, c + dc
        return False

    def get_valid_moves(self, state, player):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(state, player, row, col):
                    valid_moves.append((row, col))
        return valid_moves

    def make_move(self, state, player, row, col):
        if not self.is_valid_move(state, player, row, col):
            raise ValueError('Invalid move')
        state[row, col] = player
        state = self._flip_pieces(state, player, row, col)
        r, t = self.value_termination(state)

        return state, r, t

    def _flip_pieces(self, state, player, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self._is_valid_direction(state, player, row, col, dr, dc):
                    state = self._flip_direction(state, player, row, col, dr, dc)
        return state

    def _flip_direction(self, state, player, row, col, dr, dc):
        opponent = -player
        r, c = row + dr, col + dc
        while state[r, c] == opponent:
            state[r, c] = player
            r, c = r + dr, c + dc
        return state

    def is_done(self, state):
        v1 = self.get_valid_moves(state, 1)
        v2 = self.get_valid_moves(state, -1)
        return ((len(v1) == 0) and (len(v2) == 0))

    def winner(self, state):
        ones = np.sum(state == 1)
        mones = np.sum(state == -1)
        if ones > mones:
          return 1
        elif ones < mones:
          return -1
        return 0

    def value_termination(self, state):
        if self.is_done(state):
            return self.winner(state), True
        else:
            return 0, False

    def encoded_state(self, state):
        encoded_state = np.stack(
            (state == -1, state == 0, state == 1)
        ).astype(np.float32)

        return encoded_state
