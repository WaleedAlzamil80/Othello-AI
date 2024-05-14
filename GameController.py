from Constants import *

class GameController:
    def draw_game(board):
        GameController.draw_top_bar(board)
        GameController.draw_game_board(board)
        
        
    def draw_top_bar(board):
        pygame.draw.rect(
            WIN, Colors.TOP_BAR, ((BOARD_START_X, MARGIN, BOARD_SIZE_PIXELS, TOP_BAR_HEIGHT)))
        square_size = BOARD_SIZE_PIXELS/board.board_size
        radius = 0.8 * square_size // 2

        white_center = (BOARD_START_X + BOARD_SIZE_PIXELS * 0.1, MARGIN + TOP_BAR_HEIGHT//2)
        pygame.draw.circle(WIN, (255, 255, 255), white_center, radius)
        
        black_center = (BOARD_START_X + BOARD_SIZE_PIXELS * 0.9, MARGIN + TOP_BAR_HEIGHT//2)
        pygame.draw.circle(WIN, (0, 0, 0), black_center, radius)

        white_score = pygame.font.Font(None, 25).render(board.white_score(), True, "#FFFFFF")
        WIN.blit(white_score, white_score.get_rect(center=(white_center[0]+radius+MARGIN,white_center[1])))

        black_score = pygame.font.Font(None, 25).render(board.black_score(), True, "#FFFFFF")
        WIN.blit(black_score, white_score.get_rect(center=(black_center[0]-radius-MARGIN,black_center[1])))

    def draw_game_board(board):
        square_size = BOARD_SIZE_PIXELS/board.board_size
        for row in range(board.board_size):
            for col in range(board.board_size):
                GameController.draw_tile(row, col, board.board[row][col], square_size)
        for move in board.get_valid_moves():
            GameController.draw_valid_move(move[1], move[0], board.current_player, square_size)

    def draw_tile(row, col, value, square_size):
        tile_border = pygame.Rect(BOARD_START_X + col * square_size,
                                          BOARD_START_Y + row * square_size,
                                           square_size, square_size)
        pygame.draw.rect(WIN, (0,0,0) , tile_border, 1)
        tile = tile_border.inflate(-1, -1)
        pygame.draw.rect(WIN, Colors.BOARD, tile)
        
        circle_center = tile.center
        if value == -1:
            pygame.draw.circle(WIN, (255, 255, 255), circle_center, 0.8 * square_size // 2)
        elif value == 1:
            pygame.draw.circle(WIN, (0, 0, 0), circle_center, 0.8 * square_size // 2)

    def draw_valid_move(row, col, value, square_size):
        color = None 
        if value == -1:
            color = (255, 255, 255)
        elif value == 1:
            color = (0, 0, 0)
        pygame.draw.circle(WIN, color, 
                               (BOARD_START_X + (row + 0.5)*square_size,
                                BOARD_START_Y + (col + 0.5)*square_size,),
                                0.8 * square_size // 2, 1)
        

    def get_tile_from_pos(pos, square_size):
        x, y = pos
        if x > BOARD_START_X and x < BOARD_START_X + BOARD_SIZE_PIXELS and y > BOARD_START_Y and y < BOARD_START_Y + BOARD_SIZE_PIXELS:
            return int((y - BOARD_START_Y) // square_size), int((x - BOARD_START_X) // square_size)
        return None
    
    def click_action(board):
        pos = pygame.mouse.get_pos()
        square_size = BOARD_SIZE_PIXELS/board.board_size
        print(board.get_valid_moves())
        pos = GameController.get_tile_from_pos(pos, square_size)
        if pos != None:
            row, col = pos
            print((row , col))
            board.make_move(row , col)