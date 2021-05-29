import pygame
from pygame.locals import *
import random
import sys
import numpy as np
import time

pygame.font.init()
pygame.init()

# Game window
WIDTH, HEIGHT = 300, 335
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

#Fonts
TURN_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 40)
DRAW_FONT = pygame.font.SysFont('comicsans', 40)


#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
ORANGE = (255, 165, 0)

#FPS
FPS = 60

# X and O images and scaling
X_WIDTH, X_HEIGHT = 99, 99
O_WIDTH, O_HEIGHT = 98, 98
X_image = pygame.image.load('Assets/X.png')
X = pygame.transform.scale(X_image, (X_WIDTH, X_HEIGHT))
O_image = pygame.image.load('Assets/O.png')
O = pygame.transform.scale(O_image, (O_WIDTH, O_HEIGHT))

# Tic-Tac-Toe Board Lines 
LEFT_BOARD_LINE = [(100,0), (100,300)]
RIGHT_BOARD_LINE = [(200,0), (200,300)]
TOP_BOARD_LINE = [(0,100), (300,100)]
BOTTOM_BOARD_LINE = [(0,200), (300,200)]
BOARD_LINE_THICKNESS = 5

#Collision boxes for each Tic-tac-toe square
BOX_SIZE = (100, 100)
boxlist = []
boxlist.append(pygame.Rect((0, 0), BOX_SIZE)) #Top left
boxlist.append(pygame.Rect((100, 0), BOX_SIZE)) # Top middle
boxlist.append(pygame.Rect((200, 0), BOX_SIZE)) #Top right

boxlist.append(pygame.Rect((0, 100), BOX_SIZE)) #Middle left
boxlist.append(pygame.Rect((100, 100), BOX_SIZE)) #Middle middle
boxlist.append(pygame.Rect((200, 100), BOX_SIZE)) # Middle right

boxlist.append(pygame.Rect((0, 200), BOX_SIZE)) # Bottom left
boxlist.append(pygame.Rect((100, 200), BOX_SIZE)) # Bottom middle
boxlist.append(pygame.Rect((200, 200), BOX_SIZE)) # Bottom right


# list that represents the Tic-Tac-Toe board
board = [[' ',' ',' '], 
        [' ',' ',' '], 
        [' ',' ',' ']]


#Draws initial window with Tic-tac-toe board
def draw_window():
    WIN.fill(WHITE)
    #Draws Tic-tac-toe board
    pygame.draw.lines(WIN, BLACK, False, LEFT_BOARD_LINE, BOARD_LINE_THICKNESS)
    pygame.draw.lines(WIN, BLACK, False, RIGHT_BOARD_LINE, BOARD_LINE_THICKNESS)
    pygame.draw.lines(WIN, BLACK, False, TOP_BOARD_LINE, BOARD_LINE_THICKNESS)
    pygame.draw.lines(WIN, BLACK, False, BOTTOM_BOARD_LINE, BOARD_LINE_THICKNESS)
    pygame.display.update()

#Draws new pieces (X or O) in the corresponding spot
def draw_new_piece(piece, index):
    if piece == 'X':
        WIN.blit(X, boxlist[index])
    else:
        WIN.blit(O, boxlist[index])
    pygame.display.update()

#Returns the index of the box that the player clicked on
def get_box(mouse_pos):
    for i in range(len(boxlist)):
        if boxlist[i].collidepoint(mouse_pos):
            return i
    return -1

#Updates the 2d list that keeps track of the board
def update_board(piece, index):
    row = index // 3 # converts 1d index to 2d index
    col = index % 3 # makes my life easier
    if board[row][col] != ' ':
        return False
    board[row][col] = piece

# Changes the current turn after the player has chosen a valid move
def change_turn(turn):
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'
    return turn

# Checks board for win (3 across, down, or diagonal)
def check_for_win():
    for i in range(0,3):
        if ((board[i][0] == board[i][1] == board[i][2]) and board[i][2] != ' '):
            return True
        if ((board[0][i] == board[1][i] == board[2][i]) and board[2][i] != ' '):
            return True

    if ((board[0][0] == board[1][1] == board[2][2]) and board[2][2] != ' '):
                return True

    if ((board[0][2] == board[1][1] == board[2][0]) and board[2][0] != ' '):
                return True
    return False

# Checks if the game is a draw, (if all spots are filled)
def check_for_draw():
    for row in board:
        for i in row:
            if i == ' ':
                return False
    return True

# Renders Win text e.g: [X Won!]
def draw_winner(turn):
    winner_text = WINNER_FONT.render(turn + " Won!", 1, ORANGE)
    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()/2, (HEIGHT-25)//2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

# Renders Draw Text 
def draw_draw_game():
    draw_game_text = DRAW_FONT.render("Draw Game!", 1, ORANGE)
    WIN.blit(draw_game_text, (WIDTH//2 - draw_game_text.get_width()/2, (HEIGHT-25)//2 - draw_game_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

#Resets tictactoe board after e ach game
def reset_board():
    global board
    board = [[' ',' ',' '], 
        [' ',' ',' '], 
        [' ',' ',' ']]

# Renders Text stating whos turn it is
def draw_turn(turn):
    if turn == 'O':
        turn_text = TURN_FONT.render("Your Turn!", 1, ORANGE)
    else: 
        turn_text = TURN_FONT.render("AI Turn!", 1, ORANGE)
    #Removes the old turn_text before doing the new one
    pygame.draw.rect(WIN, WHITE, (WIDTH//2 - turn_text.get_width()/2, (HEIGHT- 20) - turn_text.get_height()/2, 125, 50))
    
    WIN.blit(turn_text, (WIDTH//2 - turn_text.get_width()/2, ((HEIGHT- 20) - turn_text.get_height()/2)))
    pygame.display.update()


def get_state(turn):
        oned_board = [j for sub in board for j in sub]
        for i in range(len(oned_board)):
            if oned_board[i] == 'X':
                oned_board[i] = 1
            elif oned_board[i] == 'O':
                oned_board[i] = 2
            else:
                oned_board[i] = 0
        if turn == 'O':
            for i in range(len(oned_board)):
                oned_board[i] += 2

        return tuple(oned_board)

def main():
    q_table = np.load('q_table.npy')
    turn = 'X'
    draw_window()
    draw_turn(turn)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        #if its the AI's turn
        if turn == 'X':
                #time.sleep(2)
                state = get_state(turn) #get the state of the current board
                index = np.argmax(q_table[state])
                if update_board(turn, index) == False: # ignore invalid choice
                        continue
                draw_new_piece(turn, index)

                if check_for_win() == True: # If there is a winner reset the game
                        draw_winner(turn)
                        reset_board()
                        running = False
                        break

                if check_for_draw() == True:
                    draw_draw_game()
                    reset_board()
                    running = False
                    break

                turn = change_turn(turn)
                draw_turn(turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if get_box(mouse_pos) == -1: # ignore invalid click
                        continue
                    else:
                        index = get_box(mouse_pos) #Index of the box that they clicked on

                    if update_board(turn, index) == False: # ignore invalid click
                        continue

                    draw_new_piece(turn, index)

                    if check_for_win() == True: # If there is a winner reset the game
                        draw_winner(turn)
                        reset_board()
                        running = False
                        break

                    if check_for_draw() == True:
                        draw_draw_game()
                        reset_board()
                        running = False
                        break

                    turn = change_turn(turn)
                    draw_turn(turn)
    main()

if __name__ == "__main__":
    main()