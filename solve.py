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
            8: Image.open('images/eight.png'),
            'mine': Image.open('images/flag.png')
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
    raw_tiles = [[t, list(pyautogui.locateAllOnScreen(TILES[t]))] for t in TILES]
    tiles = []
    for value, locations in raw_tiles:
        for location in locations:
            tiles.append({'location': location, 'value': value})
    tiles = sorted(tiles, key=lambda x: (x['location'][1], x['location'][0]))
    height = sum(1 for i in tiles if i['location'][0]==tiles[0]['location'][0])
    width = sum(1 for i in tiles if i['location'][1]==tiles[0]['location'][1])
    board = {i: {'location': tile['location'], 'neighbours': get_neighbours(i, width, height), 'value': tile['value'], 'action': None} for i, tile in enumerate(tiles)}
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
    # Check if all mines are accounted for, and reveal the rest
    if value == mines:
       for t in unclicked:
           board[t]['action'] = 'reveal'
    # Check if remaining unknown area all mines
    elif value-mines == len(unclicked):
       for t in unclicked:
           board[t]['action'] = 'flag'
           board[t]['value'] = 'mine'
    # Deductive logic
    else:
        remaining = tile['value'] - mines
        evaluable_neighbours = [n for n in tile['neighbours'] if is_evaluable(n, board)]
        for neighbour in evaluable_neighbours:
            n_tile = board[neighbour]
            n_unclicked = [t for t in n_tile['neighbours'] if board[t]['value'] is None]
            # we can only apply deductive logic if all the unclicked
            # tiles of the neighbour are also common with the current
            if len(n_unclicked) == 0 or len(set(n_unclicked).difference(set(unclicked)))!=0:
                continue
            n_remaining = n_tile['value'] - len([t for t in n_tile['neighbours'] if board[t]['value'] == 'mine'])
            # Number of remaining mines after the common ones are taken into
            # consideration
            pair_remaining = remaining - n_remaining
            unshared = set(unclicked).difference(set(n_unclicked))
            if pair_remaining == 0:
                for t in unshared:
                    board[t]['action'] = 'reveal'
            if pair_remaining == len(unshared):
                for t in unshared:
                    board[t]['action'] = 'flag'
                    board[t]['value'] = 'mine'
    return board

def flag_tile(tile_index, board):
    tile = board[tile_index]
    x, y, w, h = tile['location']
    pyautogui.moveTo(x+w/2, y+h/2, 0)
    pyautogui.press('space')

def new_board(board):
    for t in board:
        if board[t]['value'] is not None:
            return False
    return True

def sweep(num_restarts=5):
    for i in range(num_restarts):
        # pick a random tile and start the game
        board = get_board()
        if new_board(board):
            tile = random.choice(list(board.keys()))
            click_tile(tile, board)
        won = False
        flag = []
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
                if action == 'flag':
                    flag.append(tile)
                    # flag_tile(tile, board)
            # pyautogui.press('enter')
            if len(evaluable) == 0: 
                won = True
                break
            if len(actions) == 0:
#                 for f in flag:
#                     flag_tile(f, board)
                break
        if won:
            print('Winner Winner Chicken Dinner')
            break
        if i+1 != num_restarts:
            restart()

if __name__ == '__main__':
    sweep(1)

