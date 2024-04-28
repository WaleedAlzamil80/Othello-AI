import pygame
from Constants import *
from Drawer import drawer


def play():
    while True:
        WIN.fill(Colors.BACKGROUND)
        CLOCK.tick(FPS)
        drawer.draw_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()

def main():
    play()

main()