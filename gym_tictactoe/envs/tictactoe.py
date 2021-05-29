import pygame
from pygame.locals import *
import random
from random import randrange

class TicTacToeGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()

        # Game window
        self.WIDTH, self.HEIGHT = 300, 335
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")

        #Fonts
        self.TURN_FONT = pygame.font.SysFont('comicsans', 30)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 40)
        self.DRAW_FONT = pygame.font.SysFont('comicsans', 40)


        #Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0 ,0)
        self.ORANGE = (255, 165, 0)

        #FPS
        self.FPS = 60

        # X and O images and scaling
        self.X_WIDTH, self.X_HEIGHT = 99, 99
        self.O_WIDTH, self.O_HEIGHT = 98, 98
        self.X_image = pygame.image.load('Assets/X.png')
        self.X = pygame.transform.scale(self.X_image, (self.X_WIDTH, self.X_HEIGHT))
        self.O_image = pygame.image.load('Assets/O.png')
        self.O = pygame.transform.scale(self.O_image, (self.O_WIDTH, self.O_HEIGHT))

        # Tic-Tac-Toe Board Lines 
        self.LEFT_BOARD_LINE = [(100,0), (100,300)]
        self.RIGHT_BOARD_LINE = [(200,0), (200,300)]
        self.TOP_BOARD_LINE = [(0,100), (300,100)]
        self.BOTTOM_BOARD_LINE = [(0,200), (300,200)]
        self.BOARD_LINE_THICKNESS = 5

        #Collision boxes for each Tic-tac-toe square
        self.BOX_SIZE = (100, 100)
        self.boxlist = []
        self.boxlist.append(pygame.Rect((0, 0), self.BOX_SIZE)) #Top left
        self.boxlist.append(pygame.Rect((100, 0), self.BOX_SIZE)) # Top middle
        self.boxlist.append(pygame.Rect((200, 0), self.BOX_SIZE)) #Top right

        self.boxlist.append(pygame.Rect((0, 100), self.BOX_SIZE)) #Middle left
        self.boxlist.append(pygame.Rect((100, 100), self.BOX_SIZE)) #Middle middle
        self.boxlist.append(pygame.Rect((200, 100), self.BOX_SIZE)) # Middle right

        self.boxlist.append(pygame.Rect((0, 200), self.BOX_SIZE)) # Bottom left
        self.boxlist.append(pygame.Rect((100, 200), self.BOX_SIZE)) # Bottom middle
        self.boxlist.append(pygame.Rect((200, 200), self.BOX_SIZE)) # Bottom right


        # list that represents the Tic-Tac-Toe board
        self.board = [[' ',' ',' '], 
                [' ',' ',' '], 
                [' ',' ',' ']]
        self.done = False
        self.draw = False
        self.last_move_invalid = False
        self.turn = "X"
        self.winner = " "
        
    
    #Converts 2d list to 1d numpy array
    def observe(self):
        oned_board = [j for sub in self.board for j in sub]
        for i in range(len(oned_board)):
            if oned_board[i] == 'X':
                oned_board[i] = 1
            elif oned_board[i] == 'O':
                oned_board[i] = 2
            else:
                oned_board[i] = 0
        return tuple(oned_board)

    #Qlearning reward
    def evaluate(self):
        if self.draw:
            return 5
        if self.last_move_invalid:
            return -1
        if self.winner == 'X':
            return 10
        if self.done and (self.winner != 'X'):
            return -10
        return -1
    #Game over or not
    def is_done(self):
        return self.done

    #Current action (which move was chosen)
    def action(self, action):
        if self.update_board(self.turn, action) == False: # ignore invalid click
            self.last_move_invalid == True
            return False

        self.draw_new_piece(self.turn, action)
        if self.check_for_win() == True: # If there is a winner reset the game
            self.draw_winner(self.turn)
            self.done = True
            self.winner = self.turn
            return

        if self.check_for_draw() == True:
            self.draw_draw_game()
            self.done = True
            self.draw = True
            return
          
        self.last_move_invalid == False
        self.turn = self.change_turn(self.turn)
        self.draw_turn(self.turn)
        #time.sleep(1)
        action = randrange(9)
        while self.update_board(self.turn, action) == False:
            action = randrange(9)
        
        self.draw_new_piece(self.turn, action)
        if self.check_for_win() == True: # If there is a winner reset the game
            self.draw_winner(self.turn)
            self.done = True
            self.winner = self.turn
            return

        if self.check_for_draw() == True:
            self.draw_draw_game()
            self.done = True
            self.draw = True
            return
        
        self.turn = self.change_turn(self.turn)
        self.draw_turn(self.turn)


    def view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
        
        self.clock.tick(self.FPS)
        self.draw_window()
        self.draw_turn(self.turn)
    

    #Draws initial window with Tic-tac-toe board
    def draw_window(self):
        self.WIN.fill(self.WHITE)
        #Draws Tic-tac-toe board
        pygame.draw.lines(self.WIN, self.BLACK, False, self.LEFT_BOARD_LINE, self.BOARD_LINE_THICKNESS)
        pygame.draw.lines(self.WIN, self.BLACK, False, self.RIGHT_BOARD_LINE, self.BOARD_LINE_THICKNESS)
        pygame.draw.lines(self.WIN, self.BLACK, False, self.TOP_BOARD_LINE, self.BOARD_LINE_THICKNESS)
        pygame.draw.lines(self.WIN, self.BLACK, False, self.BOTTOM_BOARD_LINE, self.BOARD_LINE_THICKNESS)
        pygame.display.update()

    #Draws new pieces (X or O) in the corresponding spot
    def draw_new_piece(self, piece, index):
        if piece == 'X':
            self.WIN.blit(self.X, self.boxlist[index])
        else:
            self.WIN.blit(self.O, self.boxlist[index])
        pygame.display.update()


    #Updates the 2d list that keeps track of the board
    def update_board(self, piece, index):
        row = index // 3 # converts 1d index to 2d index
        col = index % 3 # makes my life easier
        if self.board[row][col] != ' ':
            return False
        self.board[row][col] = piece

    # Changes the current turn after the player has chosen a valid move
    def change_turn(self, turn):
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        return turn

    # Checks board for win (3 across, down, or diagonal)
    def check_for_win(self):
        for i in range(0,3):
            if ((self.board[i][0] == self.board[i][1] == self.board[i][2]) and self.board[i][2] != ' '):
                return True
            if ((self.board[0][i] == self.board[1][i] == self.board[2][i]) and self.board[2][i] != ' '):
                return True

        if ((self.board[0][0] == self.board[1][1] == self.board[2][2]) and self.board[2][2] != ' '):
                    return True

        if ((self.board[0][2] == self.board[1][1] == self.board[2][0]) and self.board[2][0] != ' '):
                    return True
        return False

    # Checks if the game is a draw, (if all spots are filled)
    def check_for_draw(self):
        for row in self.board:
            for i in row:
                if i == ' ':
                    return False
        return True

    # Renders Win text e.g: [X Won!]
    def draw_winner(self, turn):
        winner_text = self.WINNER_FONT.render(turn + " Won!", 1, self.ORANGE)
        self.WIN.blit(winner_text, (self.WIDTH//2 - winner_text.get_width()/2, (self.HEIGHT-25)//2 - winner_text.get_height()/2))
        pygame.display.update()
        #pygame.time.delay(4000)

    # Renders Draw Text 
    def draw_draw_game(self):
        draw_game_text = self.DRAW_FONT.render("Draw Game!", 1, self.ORANGE)
        self.WIN.blit(draw_game_text, (self.WIDTH//2 - draw_game_text.get_width()/2, (self.HEIGHT-25)//2 - draw_game_text.get_height()/2))
        pygame.display.update()
        #pygame.time.delay(4000)


    # Renders Text stating whos turn it is
    def draw_turn(self, turn):
        turn_text = self.TURN_FONT.render("Player " + turn + " Turn", 1, self.ORANGE)
        #Removes the old turn_text before doing the new one
        pygame.draw.rect(self.WIN, self.WHITE, (self.WIDTH//2 - turn_text.get_width()/2, (self.HEIGHT- 20) - turn_text.get_height()/2, 125, 50))
        
        self.WIN.blit(turn_text, (self.WIDTH//2 - turn_text.get_width()/2, ((self.HEIGHT- 20) - turn_text.get_height()/2)))
        pygame.display.update()

    # Randomly Decidies which player has the first move
    def choose_first_move(self):
        x = random.randint(0, 1)
        return 'X' if x == 1 else 'O'

