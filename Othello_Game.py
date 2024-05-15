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

    def stability_value(self, player):
        weights = {'stable': 1, 'semi-stable': 0, 'unstable': -1}
        stable_count = 0
        semi_stable_count = 0
        unstable_count = 0

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row, col] == player:
                    if (row == 0 or row == self.board_size - 1) and (col == 0 or col == self.board_size - 1):
                        stable_count += 1
                    else:
                        neighbors = [(row + dr, col + dc) for dr in range(-1, 2) for dc in range(-1, 2)
                                    if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size]
                        neighbor_values = [self.board[r, c] for r, c in neighbors]
                        if ' ' in neighbor_values and player in neighbor_values:
                            semi_stable_count += 1
                        else:
                            unstable_count += 1

        return weights['stable'] * stable_count + weights['semi-stable'] * semi_stable_count + weights['unstable'] * unstable_count

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
            maxCorners = 0
            minCorners = 0
            if self.board[0][0] == 1:
                maxCorners += 1
            elif self.board[0][0] == -1:
                minCorners += 1
            if self.board[0][7] == 1:
                maxCorners += 1
            elif self.board[0][7] == -1:
                minCorners += 1
            if self.board[7][0] == 1:
                maxCorners += 1
            elif self.board[7][0] == -1:
                minCorners += 1
            if self.board[7][7] == 1:
                maxCorners += 1
            elif self.board[7][7] == -1:
                minCorners += 1
            if maxCorners + minCorners != 0:
                return 100.0 * (maxCorners - minCorners) / (maxCorners + minCorners)
            else:
                return 0

        def stability():
            max_player_stability = self.stability_value(self.current_player)
            min_player_stability = self.stability_value(-self.current_player)
            return 100 * (max_player_stability - min_player_stability) / (max_player_stability + min_player_stability + 1)

        return coin_parity() + mobility() + corners_captured() + stability()

    def is_done(self):
        v1 = self.get_valid_moves()
        self.current_player *= -1
        v2 = self.get_valid_moves()
        self.current_player *= -1
        return ((len(v1) == 0) and (len(v2) == 0))

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
