from Constants import *

class drawer:
    def draw_game():
        drawer.draw_top_bar()
        drawer.draw_game_board(8,8,BOARD_SIZE/8)
        
    def draw_top_bar():
        pygame.draw.rect(
            WIN, Colors.TOP_BAR, ((BOARD_HORIZONTAL_START, MARGIN, BOARD_SIZE, TOP_BAR_HEIGHT)))

    def draw_game_board(rows, cols, square_size):
        for row in range(rows):
            for col in range(cols):
                drawer.draw_tile(row, col, -1, square_size)

    def draw_tile(row, col, value, square_size):
        tile_border = pygame.Rect(BOARD_HORIZONTAL_START + col * square_size,
                                          BOARD_VERTICAL_START + row * square_size,
                                           square_size, square_size)
        pygame.draw.rect(WIN, (0,0,0) , tile_border, 1)
        tile = tile_border.inflate(-1, -1)
        pygame.draw.rect(WIN, Colors.BOARD, tile)
        
        circle_center = tile.center
        circle_radius = 0.8 * square_size // 2
        if value == -1:
            pygame.draw.circle(WIN, (255, 255, 255), circle_center, circle_radius)
        elif value == 1:
            pygame.draw.circle(WIN, (0, 0, 0), circle_center, circle_radius)