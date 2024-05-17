import time
import numpy as np
import copy

from Constants import PLAYER_DIFFICULTY_EASY, PLAYER_DIFFICULTY_HARD, PLAYER_DIFFICULTY_MEDIUM

class Minmax:

    start_time = 0
    time_limit = 5

    def get_best_move(board, depth, alpha_beta = False, time_constrain = False):
        best_move = None
        max_eval = float('-inf') if board.current_player == 1 else float('inf')
        valid_moves = board.get_valid_moves()
        previous_board = copy.deepcopy(board.board)
        Minmax.start_time = time.time()
        depth = 0
        con = False
        while not con:
            depth += 1
            moves = []
            last_eval = max_eval
            last_move = best_move
            max_eval = float('-inf') if board.current_player == 1 else float('inf')
            for move in valid_moves:
                if con: break
                board.make_move(*move)
                if alpha_beta:
                    if time_constrain:
                        eval, con = Minmax.minimax_alpha_beta_time_constrain(depth, float('-inf'), float('inf'), False, board)
                        if con:
                            max_eval = last_eval
                            best_move = last_move
                            board.board = copy.deepcopy(previous_board)
                            board.current_player *= -1 
                            depth -=1
                            break
                    else:
                      eval = Minmax.minimax_alpha_beta(depth - 1, float('-inf'), float('inf'), False, board)
                else:
                    eval = Minmax.minimax(depth - 1, False)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1 
                moves.append((move, eval))
                if ((board.current_player == -1 and eval < max_eval) or\
                    (board.current_player == 1 and eval > max_eval)):
                    max_eval = eval
                    best_move = move
            print(moves)
        print("Depth is : ", depth)
        print(max_eval)
        return best_move

    def minimax_alpha_beta_time_constrain(depth, alpha, beta, maximizing_player, board):
        if (time.time() - Minmax.start_time) > Minmax.time_limit:
            return 0, True

        valid_moves = board.get_valid_moves()
        if depth == 0 or len(valid_moves) == 0:
            return Minmax.evaluate_heuristic(board), False

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, timed_out = Minmax.minimax_alpha_beta_time_constrain(depth - 1, alpha, beta, False, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                if timed_out:
                    return 0, True
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, False
        else:
            min_eval = float('inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, timed_out = Minmax.minimax_alpha_beta_time_constrain(depth - 1, alpha, beta, True, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                if timed_out:
                    return 0, True
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, False

    def minimax_alpha_beta(depth, alpha, beta, maximizing_player, board):
        valid_moves = board.get_valid_moves()
        if depth == 0 or len(valid_moves)==0:
            return Minmax.evaluate_heuristic(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval = Minmax.minimax_alpha_beta(depth - 1, alpha, beta, False, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval = Minmax.minimax_alpha_beta(depth - 1, alpha, beta, True, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def minimax(depth, maximizing_player, board):
        valid_moves = board.get_valid_moves()
        if not depth or len(valid_moves)==0:
            return Minmax.evaluate_heuristic()

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval = Minmax.minimax(depth - 1, False, board)
                max_eval = max(max_eval, eval)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval = Minmax.minimax(depth - 1, True, board)
                min_eval = min(min_eval, eval)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
            return min_eval

    def evaluate_heuristic(board):
        def coin_parity():
            max_player_coins = np.sum(board.board == board.current_player)
            min_player_coins = np.sum(board.board == -board.current_player)
            return 100 * (max_player_coins - min_player_coins) / (max_player_coins + min_player_coins + 1)

        def mobility():
            max_player_mobility = len(board.get_valid_moves())
            board.current_player *= -1
            min_player_mobility = len(board.get_valid_moves())
            board.current_player *= -1
            return 100 * (max_player_mobility - min_player_mobility) / (max_player_mobility + min_player_mobility + 1)

        def corners_captured():
            maxCorners = 0
            minCorners = 0
            if board.board[0][0] == 1:
                maxCorners += 1
            elif board.board[0][0] == -1:
                minCorners += 1
            if board.board[0][7] == 1:
                maxCorners += 1
            elif board.board[0][7] == -1:
                minCorners += 1
            if board.board[7][0] == 1:
                maxCorners += 1
            elif board.board[7][0] == -1:
                minCorners += 1
            if board.board[7][7] == 1:
                maxCorners += 1
            elif board.board[7][7] == -1:
                minCorners += 1
            if maxCorners + minCorners != 0:
                return 100.0 * (maxCorners - minCorners) / (maxCorners + minCorners)
            else:
                return 0

        def stability_value(board, player):
          weights = {'stable': 1, 'semi-stable': 0, 'unstable': -1}
          stable_count = 0
          semi_stable_count = 0
          unstable_count = 0

          for row in range(board.board_size):
              for col in range(board.board_size):
                  if board.board[row, col] == player:
                      if (row == 0 or row == board.board_size - 1) and (col == 0 or col == board.board_size - 1):
                          stable_count += 1
                      else:
                          neighbors = [(row + dr, col + dc) for dr in range(-1, 2) for dc in range(-1, 2)
                                      if 0 <= row + dr < board.board_size and 0 <= col + dc < board.board_size]
                          neighbor_values = [board.board[r, c] for r, c in neighbors]
                          if ' ' in neighbor_values and player in neighbor_values:
                              semi_stable_count += 1
                          else:
                              unstable_count += 1

          return weights['stable'] * stable_count + weights['semi-stable'] * semi_stable_count + weights['unstable'] * unstable_count

        def stability(board):
            max_player_stability = stability_value(board, board.current_player)
            min_player_stability = stability_value(board, -board.current_player)
            return 100 * (max_player_stability - min_player_stability) / (max_player_stability + min_player_stability + 1)
        
        # if diff == PLAYER_DIFFICULTY_EASY:
        #     return coin_parity() + mobility()
        # if diff == PLAYER_DIFFICULTY_MEDIUM:
        #     return coin_parity() + mobility() + corners_captured()
        # if diff == PLAYER_DIFFICULTY_HARD:
        return coin_parity() + mobility() + corners_captured() + stability(board)