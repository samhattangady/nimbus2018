import os
import random
import time

import pyautogui
from PIL import Image

from helpers import top_left, above, top_right, right, bottom_right, below, bottom_left, left 

TILES = {
            None: Image.open('images/unclicked.png'),
            0: Image.open('images/zero.png'),
            1: Image.open('images/one.png'),
            2: Image.open('images/two.png'),
            3: Image.open('images/three.png'),
            4: Image.open('images/four.png'),
            5: Image.open('images/five.png'),
            6: Image.open('images/six.png'),
            7: Image.open('images/seven.png'),
            8: Image.open('images/eight.png')
        }


def restart():
    pyautogui.press('f2')

def get_neighbours(i, width, height):
    functions = [top_left, above, top_right, right, bottom_right, below, bottom_left, left]
    neighbours = [f(i, width, height) for f in functions]
    return [n for n in neighbours if n is not None]

def get_board():
    # works on a fresh board, where all are unclicked. First we find all
    # the tiles, and then we arrange them in order, and find all the nieghbours
    tiles = list(pyautogui.locateAllOnScreen(TILES[None]))
    tiles = sorted(tiles, key=lambda x: (x[1], x[0]))
    height = sum(1 for i in tiles if i[0]==tiles[0][0])
    width = sum(1 for i in tiles if i[1]==tiles[0][1])
    board = {i: {'location': tile, 'neighbours': get_neighbours(i, width, height), 'value': None, 'action': None} for i, tile in enumerate(tiles)}
    return board

def read_tile_value(screen, tile):
    x, y, w, h = tile['location']
    # crop the area of the screen containing the tile of interest
    im = screen.crop((x, y, x+w, y+h))
    # compare the cropped tile to all the possible values
    for value in TILES:
        if pyautogui.locate(TILES[value], im):
            tile['value'] = value
            break

def read_full_board(board):
    screen = pyautogui.screenshot()
    for tile in board:
        if board[tile]['value'] is not None:
            # Tile has already been read before
            continue
        read_tile_value(screen, board[tile])
    return board

def click_tile_and_read(tile_index, board):
    click_tile(tile_index, board)
    screen = pyautogui.screenshot()
    read_tile_value(screen, tile)
    return read_full_board(board)

def click_tile(tile_index, board):
    tile = board[tile_index]
    x, y, w, h = tile['location']
    pyautogui.click(x=x+w/2, y=y+h/2)

def is_evaluable(tile_index, board):
    # A tile is evaluable if it has a known value and it has atleast 
    # one neighbour with an unknown value
    tile = board[tile_index]
    is_clicked = tile['value'] is not None
    is_not_mine = tile['value'] is not 'mine'
    has_unclicked_neighbour = None in [board[t]['value'] for t in tile['neighbours']]
    return is_clicked and has_unclicked_neighbour and is_not_mine

def evaluate(tile_index, board):
    # To evaluate a single tile, we need its value, number of neighbouring
    # mines, and number of unknown neighbours. If the number of mines is
    # equal to the value, then all the unknown neighbours are not mines.
    # If the number of unknown neighbours is equal to the difference between
    # the value and the number of mines, then all the remaining unclicked
    # neighbours are mines.
    tile = board[tile_index]
    value = tile['value']
    unclicked = [t for t in tile['neighbours'] if board[t]['value'] is None]
    mines = len([t for t in tile['neighbours'] if board[t]['value'] == 'mine'])
    if value == mines:
       for t in unclicked:
           # board = click_tile_and_read(t, board)
           board[t]['action'] = 'reveal'
           # click_tile(t, board)
    if value-mines == len(unclicked):
       for t in unclicked:
           # flag_tile(t, board)
           board[t]['action'] = 'flag'
           board[t]['value'] = 'mine'
    return board

def flag_tile(tile_index, board):
    tile = board[tile_index]
    x, y, w, h = tile['location']
    pyautogui.moveTo(x+w/2, y+h/2, 0)
    pyautogui.press('space')

def sweep(num_restarts=5):
    for i in range(num_restarts):
        # pick a random tile and start the game
        board = get_board()
        won = False
        tile = random.choice(list(board.keys()))
        click_tile(tile, board)
        while True:
            board = read_full_board(board)
            # generate a list of all the tiles that should be evaluated
            evaluable = [tile for tile in board if is_evaluable(tile, board)]
            for tile in evaluable:
                board = evaluate(tile, board)
            actions = []
            for tile in board:
                if board[tile]['action'] == 'reveal':
                    board[tile]['action'] = None
                    actions.append((tile, 'reveal'))
                if board[tile]['action'] == 'flag':
                    board[tile]['action'] = None
                    actions.append((tile, 'flag'))
            for tile, action in actions:
                if action == 'reveal':
                    click_tile(tile, board)
            # pyautogui.press('enter')
            if len(evaluable) == 0: 
                won = True
                break
            if len(actions) == 0:
                break
        if won:
            print('Winner Winner Chicken Dinner')
            break
        restart()

if __name__ == '__main__':
    sweep()

