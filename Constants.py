import pygame

WIDTH, HEIGHT = 800, 700
FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Othello')
CLOCK = pygame.time.Clock()


MARGIN = 0.04 * HEIGHT
TOP_BAR_HEIGHT = 0.12 * HEIGHT
BOARD_SIZE_PIXELS = HEIGHT - 3 * MARGIN - TOP_BAR_HEIGHT
BOARD_START_Y = 2 * MARGIN + TOP_BAR_HEIGHT
BOARD_START_X = (WIDTH-BOARD_SIZE_PIXELS)/2

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.image.load("assets/Background.png")

class Colors:
    BACKGROUND = (35, 35, 35)
    TOP_BAR = (125, 125, 125)
    BOARD = (0, 145, 100)


PLAYER_TYPE_HUMAN = "human"
PLAYER_TYPE_MONTE_CARLO = "carlo"
PLAYER_TYPE_MINMAX = "minmax"

PLAYER_DIFFICULTY_EASY = "easy"
PLAYER_DIFFICULTY_MEDIUM = "medium"
PLAYER_DIFFICULTY_HARD = "hard"
