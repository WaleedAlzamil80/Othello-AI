import time
import numpy as np
import copy

from Constants import PLAYER_DIFFICULTY_EASY, PLAYER_DIFFICULTY_HARD, PLAYER_DIFFICULTY_MEDIUM

class Minmax:

    start_time = 0
    time_limit = 5
    difficulty = PLAYER_DIFFICULTY_EASY
    leafs_visited = 0

    def get_best_move_time_constrained(board):
        best_move = None
        Minmax.start_time = time.time()
        depth = 0
        con = False
        while not con:
            depth += 1
            last_move = best_move
            _, move, con = Minmax.minimax_alpha_beta_time_constrain(depth, float('-inf'), float('inf'), board.current_player == 1, board)
            if con:
                best_move = last_move
            else:
                best_move = move
        print("Depth is : ", depth)
        return best_move
    
    def get_best_move(board, depth, alpha_beta = False):
        best_move = None
        if alpha_beta:
            _, best_move = Minmax.minimax_alpha_beta(depth, float('-inf'), float('inf'), board.current_player == 1, board)
        else:
            _, best_move = Minmax.minimax(depth, board.current_player == 1, board)
        print("Depth is : ", depth)
        return best_move
    

    def minimax_alpha_beta_time_constrain(depth, alpha, beta, maximizing_player, board):
        if (time.time() - Minmax.start_time) > Minmax.time_limit:
            return 0, (), True

        valid_moves = board.get_valid_moves()
        if depth == 0 or len(valid_moves) == 0:
            return Minmax.evaluate_heuristic(board), (), False

        if maximizing_player:
            max_eval = float('-inf')
            max_move = None
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, _, timed_out = Minmax.minimax_alpha_beta_time_constrain(depth - 1, alpha, beta, False, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                if timed_out:
                    return 0, (), True
                if max_eval < eval:
                    max_eval = eval
                    max_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, max_move, False
        else:
            min_eval = float('inf')
            min_move = None
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, _, timed_out = Minmax.minimax_alpha_beta_time_constrain(depth - 1, alpha, beta, True, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                if timed_out:
                    return 0, (), True
                if min_eval > eval:
                    min_eval = eval
                    min_move = move
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, min_move, False

    def minimax_alpha_beta(depth, alpha, beta, maximizing_player, board):
        valid_moves = board.get_valid_moves()
        if depth == 0 or len(valid_moves)==0:
            Minmax.leafs_visited+=1
            return Minmax.evaluate_heuristic(board), ()

        if maximizing_player:
            max_eval = float('-inf')
            max_move = None
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, _ = Minmax.minimax_alpha_beta(depth - 1, alpha, beta, False, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                if max_eval < eval:
                    max_eval = eval
                    max_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, max_move
        else:
            min_eval = float('inf')
            min_move = None
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, _ = Minmax.minimax_alpha_beta(depth - 1, alpha, beta, True, board)
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
                if min_eval > eval:
                    min_eval = eval
                    min_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, min_move

    def minimax(depth, maximizing_player, board):
        valid_moves = board.get_valid_moves()
        if not depth or len(valid_moves)==0:
            Minmax.leafs_visited+=1
            return Minmax.evaluate_heuristic(board),()

        if maximizing_player:
            max_eval = float('-inf')
            max_move = None
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, _ = Minmax.minimax(depth - 1, False, board)
                if max_eval < eval:
                    max_eval = eval
                    max_move = move
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
            return max_eval, max_move
        else:
            min_eval = float('inf')
            min_move = None
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval, _ = Minmax.minimax(depth - 1, True, board)
                if min_eval > eval:
                    min_eval = eval
                    min_move = move
                board.board = copy.deepcopy(previous_board)
                board.current_player *= -1
            return min_eval, min_move

    def evaluate_heuristic(board):
        def coin_parity():
            max_player_coins = board.black_score()
            min_player_coins = board.white_score()
            return 100 * (max_player_coins - min_player_coins) / (max_player_coins + min_player_coins + 1)

        def mobility():
            if(board.current_player == 1):
                max_player_mobility = len(board.get_valid_moves())
                board.current_player *= -1
                min_player_mobility = len(board.get_valid_moves())
                board.current_player *= -1
            elif(board.current_player == -1):
                min_player_mobility = len(board.get_valid_moves())
                board.current_player *= -1
                max_player_mobility = len(board.get_valid_moves())
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
            max_player_stability = stability_value(board, 1)
            min_player_stability = stability_value(board, -1)
            return 100 * (max_player_stability - min_player_stability) / (max_player_stability + min_player_stability + 1)
        
        if Minmax.difficulty == PLAYER_DIFFICULTY_EASY:
            return coin_parity()
        if Minmax.difficulty == PLAYER_DIFFICULTY_MEDIUM:
            return coin_parity() + stability(board)
        if Minmax.difficulty == PLAYER_DIFFICULTY_HARD:
            return coin_parity() + mobility() + corners_captured() + stability(board)