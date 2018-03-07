#!/usr/bin/env python3

import sys
import pygame
from pygame.locals import *
from sys import exit
import random

screen_span = 360 # screen width and height are equal

coin = random.randint(0, 1)

if coin == 0:
    player_turn = True
else:
    player_turn = False

ENDGAME = False

winner = '_' # could be 'x' or 'o'

# list of board spaces; '_' represents an empy space
# like board[row-1][col-1]
board = [
    ["_", "_", "_"],
    ["_", "_", "_"],
    ["_", "_", "_"]
]


class Toe:

    def __init__(self, x, y, col, row, img):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.img = img

    def update(self):
        screen.blit(self.img, (self.x, self.y))


def check_x(x):
    '''returns the column that the move was made in'''
    if x >= 0 and x < 120:
        return 1 # move is in column 1
    elif x >= 120 and x < 240:
        return 2 # move is in column 2
    elif x >= 240 and x < 360:
        return 3 # move is in column 3


def check_y(y):
    '''returns the row that the move was made in'''
    if y >= 0 and y < 120:
        return 1 # move is in row 1
    elif y >= 120 and y < 240:
        return 2 # move is in row 2
    elif y >= 240 and y < 360:
        return 3 # move is in row 3


def check_move(col, row, move_maker):
    '''makes sure that the move is legal; also
       records what player (x or o) made the move'''
    global board

    # board indexes must be in range [0, 3], not [1, 4]
    if board[row - 1][col - 1] == '_':
        if move_maker == 'human':
            # if move maker was human, place an 'x' and return true
            board[row-1][col-1] = 'x'
            return True
        elif move_maker == 'computer':
            # if move maker was the computer, place an 'o' and return true
            board[row-1][col-1] = 'o'
            return True
    else:
        return False # return false if board space was taken


def place_move(col, row, img):
    '''final function of the move-making functions;
       actually places the move into moves list'''
    global moves

    # determine x coordinate for image rendering
    if col == 1:
        x = 5
    elif col == 2:
        x = 125
    elif col == 3:
        x = 245

    # determine y coordinate for image rendering
    if row == 1:
        y = 5
    elif row == 2:
        y = 125
    elif row == 3:
        y = 245

    # place/create the move
    moves.append(Toe(x, y, col, row, img))


def get_move(position, move_maker):
    '''first move-making function; makes sure that the
       move is legal before allowing one to be made'''
    global player_turn
    global x_spaces
    global o_spaces

    x, y = position

    col = check_x(x)
    row = check_y(y)

    legal_move = check_move(col, row, move_maker)

    if legal_move is True:
        # check who's making the move
        if move_maker == 'human':
            place_move(col, row, x_img)
            player_turn = False # change turn
        elif move_maker == 'computer':
            place_move(col, row, o_img)
            player_turn = True # change turn
    else:
        return


def check_for_win():
    '''checks the board for three continuous x's or o's'''
    global board
    global winner
    global ENDGAME

    # across
    if board[0][0] == board[0][1] == board[0][2] != '_':
        winner = board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] != '_':
        winner = board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] != '_':
        winner = board[2][0]

    # down
    elif board[0][0] == board[1][0] == board[2][0] != '_':
        winner = board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] != '_':
        winner = board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] != '_':
        winner = board[0][2]

    # diagonal
    elif board[0][0] == board[1][1] == board[2][2] != '_':
        winner = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != '_':
        winner = board[0][2]

    if winner == 'x' or winner == 'o':
        ENDGAME = True


#******* Setting up game ********
pygame.init()

#******* Setting up screen ******
screen = pygame.display.set_mode((screen_span, screen_span))
pygame.display.set_caption('Tic Tac Toe')

#******* Setting up images ******
x_img = pygame.image.load('x.png').convert()
o_img = pygame.image.load('zero.png').convert()
background = pygame.image.load('board.png').convert()

#******* List of X's and O's *****
moves = []

#******** Setting up clock ********
clock = pygame.time.Clock()

# ********* Game Loop **********
while ENDGAME is False:
    # check if player closed game
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONUP and player_turn is True:
            pos = pygame.mouse.get_pos()
            get_move(pos, 'human')# 'x'= X image, 'human'= human

    screen.fill((255,255,255))
    screen.blit(background, (0,0))

    if player_turn is False:
        x = random.randint(10, 350)
        y = random.randint(10, 350)
        get_move((x, y), 'computer') # 'o'= O image, 'computer'= computer

    for move in moves:
        move.update()

    check_for_win()

    pygame.display.update()

    # 60 frames per second
    clock.tick(60)


# ********* End game message **********
if winner == 'x':
    message = 'X Wins!!!'
elif winner == 'o':
    message = 'O Wins!'

while True:
    # check if player closed game
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill((255, 255, 255))

    font = pygame.font.Font(None, 36)
    text = font.render(message, 1, (10,10,10))
    screen.blit(text, (25, 25))

    pygame.display.update()