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
        depth = 1
        _, best_move = Minmax.minimax_alpha_beta(depth, float('-inf'), float('inf'), board.current_player == 1, board)
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
            temp = board.current_player
            board.current_player = 1
            max_player_mobility = len(board.get_valid_moves())
            board.current_player = -1
            min_player_mobility = len(board.get_valid_moves())
            board.current_player = temp
            if max_player_mobility + min_player_mobility != 0:
                return 100 * (max_player_mobility - min_player_mobility) / (max_player_mobility + min_player_mobility + 1)
            return 0

        def corners_captured(board):
            corners = [(0,0), (0,7), (7,0), (7,7)]
            max_corners = sum([1 for x, y in corners if board[x, y] == 1])
            min_corners = sum([1 for x, y in corners if board[x, y] == -1])
            if max_corners + min_corners != 0:
                return 100 * (max_corners - min_corners) / (max_corners + min_corners)
            return 0

        def stability(board, player):
            stable_discs = np.zeros_like(board)
            directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]

            def mark_stable(x, y, player):
                if stable_discs[x, y] != 0:
                    return
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8 and board[nx, ny] == player:
                        mark_stable(nx, ny, player)
                stable_discs[x, y] = player

            for x in range(8):
                if board[x, 0] == player:
                    mark_stable(x, 0, player)
                if board[x, 7] == player:
                    mark_stable(x, 7, player)
            for y in range(8):
                if board[0, y] == player:
                    mark_stable(0, y, player)
                if board[7, y] == player:
                    mark_stable(7, y, player)

            player_stable = np.sum(stable_discs == player)
            opponent_stable = np.sum(stable_discs == -player)
            
            if player_stable + opponent_stable != 0:
                return 100 * (player_stable - opponent_stable) / (player_stable + opponent_stable)
            return 0

        return coin_parity() + mobility() + corners_captured(board.board)

        # if Minmax.difficulty == PLAYER_DIFFICULTY_EASY:
        #     return mobility()
        # if Minmax.difficulty == PLAYER_DIFFICULTY_MEDIUM:
        #     return coin_parity() + mobility()
        # if Minmax.difficulty == PLAYER_DIFFICULTY_HARD:
        