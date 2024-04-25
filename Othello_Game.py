import numpy as np
import copy

class OthelloGame:
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

    def set_state(self, state, to_play):
        self.board = state
        self.current_player = to_play

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
            raise ValueError('Invalid move')
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
        return reward

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

    def play_two_players(self):
        while True:
            print("Current board:")
            print(self.board)
            ones = np.sum(self.board == 1)
            mones = np.sum(self.board == -1)
            print("Player 1: ", ones)
            print("Player -1: ", mones)
            print("Player", self.current_player, "to move.")
            valid_moves = self.get_valid_moves()
            if not valid_moves:
                print("No valid moves. Skipping turn.")
                self.current_player *= -1
                continue

            print("Valid moves:", valid_moves)
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                if (row, col) in valid_moves:
                    self.make_move(row, col)
                else:
                    print("Invalid move. Try again.")
            except:
                print("Enter a valid square.")

    def evaluate_heuristic(self):
        def coin_parity():
            max_player_coins = np.sum(self.board == self.current_player)
            min_player_coins = np.sum(self.board == -self.current_player)
            return 100 * (max_player_coins - min_player_coins) / (max_player_coins + min_player_coins + 1)

        def mobility():
            max_player_mobility = len(self.get_valid_moves())
            self.current_player *= -1
            min_player_mobility = len(self.get_valid_moves())
            self.current_player *= -1
            return 100 * (max_player_mobility - min_player_mobility) / (max_player_mobility + min_player_mobility + 1)

        def corners_captured():
            return 0

        def stability():
            return 0

        return coin_parity() + mobility() + corners_captured() + stability()

    def is_done(self):
        # Check if game is over (no valid moves for either player)
        return False  # Placeholder

    def minimax_alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0:
            self.current_player *= -1
            return self.evaluate_heuristic()

        valid_moves = self.get_valid_moves()
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(self.board)
                self.make_move(*move)
                eval = self.minimax_alpha_beta(depth - 1, alpha, beta, False)
                self.board = previous_board
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.current_player *= -1
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(self.board)
                self.make_move(*move)
                eval = self.minimax_alpha_beta(depth - 1, alpha, beta, True)
                self.board = copy.deepcopy(previous_board)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.current_player *= -1
            return min_eval

    def minimax(self, depth, maximizing_player):
        if not depth:
            self.current_player *= -1
            return self.evaluate_heuristic()

        valid_moves = self.get_valid_moves()
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(self.board)
                self.make_move(*move)
                eval = self.minimax(depth - 1, False)
                max_eval = max(max_eval, eval)
                self.board = copy.deepcopy(previous_board)

            self.current_player *= -1
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(self.board)
                self.make_move(*move)
                eval = self.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
                self.board = copy.deepcopy(previous_board)

            self.current_player *= -1
            return min_eval

    def get_best_move(self, depth, alpha_beta = False):
        best_move = None
        max_eval = float('-inf')
        valid_moves = self.get_valid_moves()
        previous_board = copy.deepcopy(self.board)
        for move in valid_moves:
            self.make_move(*move)
            if alpha_beta:
                eval = self.minimax_alpha_beta(depth - 1, float('-inf'), float('inf'), False)
            else:
                eval = self.minimax(depth - 1, False)
            self.board = copy.deepcopy(previous_board)

            if eval > max_eval:
                max_eval = eval
                best_move = move

        return best_move

    def play_with_ai(self, depth = 3, alpha_beta = False):
        while True:
            print("Current board:")
            print(self.board)
            print("Player", self.current_player, "to move.")
            if self.current_player == 1:
                valid_moves = self.get_valid_moves()
                if valid_moves:
                    print("Valid moves:", valid_moves)
                    row = int(input("Enter row: "))
                    col = int(input("Enter column: "))
                    if (row, col) in valid_moves:
                        print(row, col)
                        self.make_move(row, col)
                    else:
                        print("Invalid move. Try again.")
                else:
                    print("No valid moves. Skipping turn.")
                    self.current_player *= -1
                    continue
            else:
                print("AI is thinking...")
                valid_moves = self.get_valid_moves()
                if valid_moves:
                    print("Valid moves:", valid_moves)

                row, col = self.get_best_move(depth=depth, alpha_beta = alpha_beta)
                self.make_move(row, col)

game = OthelloGame()
# game.play_two_players()
game.play_with_ai(depth = 4)