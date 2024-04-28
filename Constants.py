import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Othello')
CLOCK = pygame.time.Clock()


MARGIN = 0.04 * HEIGHT
TOP_BAR_HEIGHT = 0.12 * HEIGHT
BOARD_SIZE = HEIGHT - 3 * MARGIN - TOP_BAR_HEIGHT
BOARD_VERTICAL_START = 2 * MARGIN + TOP_BAR_HEIGHT
BOARD_HORIZONTAL_START = (WIDTH-BOARD_SIZE)/2

class Colors:
    BACKGROUND = (35, 35, 35)
    TOP_BAR = (50, 50, 50)
    BOARD = (0, 145, 100)



