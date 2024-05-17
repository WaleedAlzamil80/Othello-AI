import pygame, sys
from Board import Board
from Constants import *
from GameController import GameController
from Button import Button
from MCTs.MCTs import MCTs
from Minmax import Minmax
# from RL.MCTs_Actor_Critic import MCTs_RL
# from RL.Nets import ResNet
from rules import Rules

first_player = ""
first_player_diff = ""
second_player = ""
second_player_diff = ""

def pause(board):
    while True:
        SCREEN.fill(Colors.BACKGROUND)
        CLOCK.tick(FPS)
        GameController.draw_game(board)
        button_height = SMALL_BUTTON_IMAGE.get_rect().height
        resume_button = Button(image=SMALL_BUTTON_IMAGE, pos=(BOARD_BUTTON_CENTER, MARGIN + button_height), 
                            text_input="RESUME", font=get_font(30), base_color="#000000", hovering_color="White")
        resume_button.changeColor(pygame.mouse.get_pos())
        resume_button.update(SCREEN)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(pygame.mouse.get_pos()):
                    return

def game_end_screen(board):
    while True:
        SCREEN.fill(Colors.BACKGROUND)
        CLOCK.tick(FPS)
        GameController.draw_game(board)
        button_height = SMALL_BUTTON_IMAGE.get_rect().height
        restart_button = Button(image=SMALL_BUTTON_IMAGE, pos=(BOARD_BUTTON_CENTER,MARGIN + button_height), 
                            text_input="RESTART", font=get_font(30), base_color="#000000", hovering_color="White")
        main_menu_button = Button(image=SMALL_BUTTON_IMAGE, pos=(BOARD_BUTTON_CENTER, 2 * ( MARGIN + button_height)), 
                            text_input="MAIN_MENU", font=get_font(30), base_color="#000000", hovering_color="White")
        for button in [restart_button, main_menu_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.checkForInput(pygame.mouse.get_pos()):
                    return 0
                elif restart_button.checkForInput(pygame.mouse.get_pos()):
                    return 1
                    
def play():
    rules = Rules()
    board = Board(rules)
    while True:
        SCREEN.fill(Colors.BACKGROUND)
        CLOCK.tick(FPS)
        GameController.draw_game(board)
        button_height = SMALL_BUTTON_IMAGE.get_rect().height
        pause_button = Button(image=SMALL_BUTTON_IMAGE, pos=(BOARD_BUTTON_CENTER, MARGIN + button_height), 
                            text_input="PAUSE", font=get_font(30), base_color="#000000", hovering_color="White")
        restart_button = Button(image=SMALL_BUTTON_IMAGE, pos=(BOARD_BUTTON_CENTER, 2 * ( MARGIN + button_height)), 
                            text_input="RESTART", font=get_font(30), base_color="#000000", hovering_color="White")
        main_menu_button = Button(image=SMALL_BUTTON_IMAGE, pos=(BOARD_BUTTON_CENTER, 3 * ( MARGIN + button_height)), 
                            text_input="MAIN_MENU", font=get_font(30), base_color="#000000", hovering_color="White")
        for button in [pause_button, restart_button, main_menu_button]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.checkForInput(pygame.mouse.get_pos()):
                    pause(board)
                elif restart_button.checkForInput(pygame.mouse.get_pos()):
                    board = Board(rules)
                elif main_menu_button.checkForInput(pygame.mouse.get_pos()):
                    return
                elif ((board.current_player == 1 and first_player == PLAYER_TYPE_HUMAN)
                     or (board.current_player == -1 and second_player == PLAYER_TYPE_HUMAN)):
                    GameController.click_action(board)
        
        if board.is_done(): 
            state = game_end_screen(board) 
            if state == 1: 
                board = Board(rules)
            elif state == 0:
                return
        elif(board.current_player == 1):
            print("first player" + first_player + first_player_diff)
            if(len(board.get_valid_moves()) == 0):
                board.current_player *= -1
            elif(first_player == PLAYER_TYPE_MINMAX):
                Minmax.time_limit = 1 if first_player_diff == PLAYER_DIFFICULTY_EASY else \
                2 if first_player_diff == PLAYER_DIFFICULTY_MEDIUM else 3
                # Minmax.leafs_visited = 0
                row, col = Minmax.get_best_move_time_constrained(board= board) # modified
                # row, col = Minmax.get_best_move(board= board, depth=3, alpha_beta = False) # modified
                # print("leafs: ", Minmax.leafs_visited)
                print(row,"---", col)
                board.make_move(row , col)
            elif(first_player == PLAYER_TYPE_MONTE_CARLO):
                mcts = MCTs(rules, 2000)
                row, col = mcts.action(board.board,board.current_player)
                board.make_move(row , col)
            # elif(first_player == PLAYER_TYPE_RL):
            #     pass
            #     model = ResNet(4, 64)
            #     state_dict = torch.load("RL/SavedModels/model.pt", map_location = torch.device('cpu'))
            #     model.load_state_dict(state_dict)
            #     rl = MCTs_RL(rules, 2000,model, "cpu", False) 
        elif (board.current_player == -1):
            print("second_player" + second_player + second_player_diff)
            if(len(board.get_valid_moves()) == 0):
                board.current_player *= -1
            elif(second_player == PLAYER_TYPE_MINMAX):
                Minmax.time_limit = 1 if second_player_diff == PLAYER_DIFFICULTY_EASY else \
                2 if second_player_diff == PLAYER_DIFFICULTY_MEDIUM else 3
                # Minmax.leafs_visited = 0
                row, col = Minmax.get_best_move_time_constrained(board= board)
                # row, col = Minmax.get_best_move(board= board, depth=3, alpha_beta = False)
                # print("leafs: ", Minmax.leafs_visited)
                print(row,"---", col)
                board.make_move(row , col)
            elif(second_player == PLAYER_TYPE_MONTE_CARLO):
                mcts = MCTs(rules, 2000)
                row, col = mcts.action(board.board,board.current_player)
                board.make_move(row , col)

def get_font(size):
    return pygame.font.Font(None, size)
 
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
        #                     text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        # for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
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
                # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     options()
                #quit button click
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()    

def mode_menu(player_num):
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Text = "Select First Player (black)"
        if player_num == 2:
            Text = "Select Second Player (white)"

        MENU_TEXT = get_font(75).render(Text, True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        HUMAN_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Human", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        MINMAX_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 380), 
                            text_input="MINMAX", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        CARLO_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 510), 
                            text_input="Monte Carlo", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        # RF_BUTTON = Button(image=pygame.image.load("assets/SmallRect.png"), pos=(600, 510), 
        #                     text_input="Reinforcement Learning", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
                            

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
                        return
                    else:
                        second_player = PLAYER_TYPE_MINMAX
                        difficulty_menu(2)
                        return
                #options button click
                if HUMAN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player = PLAYER_TYPE_HUMAN
                        mode_menu(2)
                        return
                    else:
                        second_player = PLAYER_TYPE_HUMAN
                        play()
                        return
                #quit button click
                if CARLO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player = PLAYER_TYPE_MONTE_CARLO
                        mode_menu(2)
                        return
                    else:
                        second_player = PLAYER_TYPE_MONTE_CARLO
                        play()
                        return
                # if RF_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     if player_num == 1:
                #         first_player = PLAYER_TYPE_MONTE_CARLO
                #         mode_menu(2)
                #         return
                #     else:
                #         second_player = PLAYER_TYPE_MONTE_CARLO
                #         play()
                #         return

        pygame.display.update()    

def difficulty_menu(player_num):
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("Select Difficulty", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Easy", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 380), 
                            text_input="Medium", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 510), 
                            text_input="Hard", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
                            

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
            global first_player_diff, second_player_diff
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_EASY
                        mode_menu(2)
                        return
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_EASY
                        # print("first_player, first_player_diff, second_player, second_player_diff")
                        # print(first_player, first_player_diff, second_player, second_player_diff)
                        # print("first_player, first_player_diff, second_player, second_player_diff")
                        play()
                        return
                #options button click
                if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_MEDIUM
                        mode_menu(2)
                        return
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_MEDIUM
                        play()
                        return
                #quit button click
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_HARD
                        mode_menu(2)
                        return
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_HARD
                        play()
                        return
        pygame.display.update()    

def options():
    pass

main_menu()