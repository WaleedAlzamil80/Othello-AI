import pygame
from Board import Board
from Constants import *
from GameController import GameController


def play():
    board = Board()
    while True:
        WIN.fill(Colors.BACKGROUND)
        CLOCK.tick(FPS)
        GameController.draw_game(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                GameController.click_action(board)
        pygame.display.flip()

def main():
    play()

main()