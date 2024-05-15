import pygame, sys
from Board import Board
from Constants import *
from GameController import GameController
from Button import Button
from Minmax import Minmax

first_player = ""
first_player_diff = ""
second_player = ""
second_player_diff = ""

def play():
    board = Board()
    while True:
        WIN.fill(Colors.BACKGROUND)
        CLOCK.tick(FPS)
        GameController.draw_game(board)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ((board.current_player == 1 and first_player == PLAYER_TYPE_HUMAN)
                     or (board.current_player == -1 and second_player == PLAYER_TYPE_HUMAN)):
                    GameController.click_action(board)
        
        if board.is_done(): 
            print('done')
        elif(board.current_player == 1):
            print("first player" + first_player)
            if(len(board.get_valid_moves()) == 0):
                board.current_player *= -1
            elif(first_player == PLAYER_TYPE_MINMAX):
                row, col = Minmax.get_best_move(board= board, depth=3, alpha_beta = True)
                if(row == None): print('hello');continue
                board.make_move(row , col)
            elif(first_player == PLAYER_TYPE_MONTE_CARLO):
                pass #here we should call montecarlo algorithm
        elif (board.current_player == -1):
            print("second_player" + second_player)
            if(len(board.get_valid_moves()) == 0):
                board.current_player *= -1
            elif(second_player == PLAYER_TYPE_MINMAX):
                row, col = Minmax.get_best_move(board= board, depth=3, alpha_beta = True)
                board.make_move(row , col)
            elif(second_player == PLAYER_TYPE_MONTE_CARLO):
                pass #here we should call montecarlo algorithm

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
                    mode_menu(1)
                #options button click
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                #quit button click
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()    

def mode_menu(player_num):
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Text = "Select First Player"
        if player_num == 2:
            Text = "Select Second Player"

        MENU_TEXT = get_font(100).render(Text, True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        HUMAN_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Human", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MINMAX_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
                            text_input="MINMAX", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CARLO_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 550), 
                            text_input="Monte Carlo", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
                            

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        for button in [HUMAN_BUTTON, MINMAX_BUTTON, CARLO_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            
            global first_player, second_player
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if MINMAX_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player = PLAYER_TYPE_MINMAX
                        difficulty_menu(1)
                    else:
                        second_player = PLAYER_TYPE_MINMAX
                        difficulty_menu(2)
                #options button click
                if HUMAN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player = PLAYER_TYPE_HUMAN
                        mode_menu(2)
                    else:
                        second_player = PLAYER_TYPE_HUMAN
                        play()
                #quit button click
                if CARLO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player = PLAYER_TYPE_MONTE_CARLO
                        difficulty_menu(1)
                    else:
                        second_player = PLAYER_TYPE_MONTE_CARLO
                        difficulty_menu(2)

        pygame.display.update()    

def difficulty_menu(player_num):
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
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_EASY
                        mode_menu(2)
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_EASY
                        play()
                #options button click
                if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_MEDIUM
                        mode_menu(2)
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_MEDIUM
                        play()
                #quit button click
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_HARD
                        mode_menu(2)
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_HARD
                        play()
        pygame.display.update()    

def options():
    pass

main_menu()