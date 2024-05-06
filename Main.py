import pygame, sys
from Board import Board
from Constants import *
from GameController import GameController
from Button import Button

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

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(None, size)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_menu()
                #options button click
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                #quit button click
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()    

def mode_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Select Mode", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        SINGLE_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Single Player", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
                            text_input="Multiplayer", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 550), 
                            text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
                            

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        for button in [SINGLE_BUTTON, MULTIPLAYER_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    difficulty_menu()
                #options button click
                if SINGLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                #quit button click
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()    

def difficulty_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Select Mode", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Easy", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
                            text_input="Medium", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 550), 
                            text_input="Hard", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
                            

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                #options button click
                if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                #quit button click
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()

        pygame.display.update()    

main_menu()