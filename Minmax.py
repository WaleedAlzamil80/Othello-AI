
import numpy as np
import copy

class Minmax:

    def get_best_move(board, depth, alpha_beta = False):
        best_move = None
        max_eval = float('-inf')
        valid_moves = board.get_valid_moves()
        previous_board = copy.deepcopy(board.board)
        for move in valid_moves:
            print(move)
            board.make_move(*move)
            if alpha_beta:
                eval = Minmax.minimax_alpha_beta(depth - 1, float('-inf'), float('inf'), False, board)
            else:
                eval = Minmax.minimax(depth - 1, False)
            board.board = copy.deepcopy(previous_board)

            if eval > max_eval:
                max_eval = eval
                best_move = move

        return best_move

    def minimax_alpha_beta(depth, alpha, beta, maximizing_player, board):
        valid_moves = board.get_valid_moves()
        if depth == 0 or len(valid_moves)==0:
            board.current_player *= -1
            return Minmax.evaluate_heuristic(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval = Minmax.minimax_alpha_beta(depth - 1, alpha, beta, False, board)
                board.board = previous_board
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            board.current_player *= -1
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                previous_board = copy.deepcopy(board.board)
                board.make_move(*move)
                eval = Minmax.minimax_alpha_beta(depth - 1, alpha, beta, True, board)
                board.board = copy.deepcopy(previous_board)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            board.current_player *= -1
            return min_eval

    def minimax(depth, maximizing_player, board):
        valid_moves = board.get_valid_moves()
        if not depth or len(valid_moves)==0:
            board.current_player *= -1
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
            return 0

        def stability():
            return 0

        return coin_parity() + mobility() + corners_captured() + stability()
