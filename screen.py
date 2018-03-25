import os
import random
import time

import pyautogui
import pyscreenshot
from PIL import Image

# TILES = {
            # None: Image.open('images/unclicked.png'),
            # 0: Image.open('images/zero.png'),
            # 1: Image.open('images/one.png'),
            # 2: Image.open('images/two.png'),
            # 3: Image.open('images/three.png'),
            # 4: Image.open('images/four.png'),
            # 5: Image.open('images/five.png'),
            # 6: Image.open('images/six.png'),
            # 7: Image.open('images/seven.png'),
            # 8: Image.open('images/eight.png')
        # }
TILES = {
            None: 'images/unclicked.png',
            0: 'images/zero.png',
            1: 'images/one.png',
            2: 'images/two.png',
            3: 'images/three.png',
            4: 'images/four.png',
            5: 'images/five.png',
            6: 'images/six.png',
            7: 'images/seven.png',
            8: 'images/eight.png'
        }


def restart():
    pyautogui.press('f2')

def game_on():
    return bool(pyautogui.locateCenterOnScreen('images/smiley.png'))

def left(i, width, height):
    if i % width != 0:
        # Not in col 1
        return i-1

def right(i, width, height):
    if (i+1) % width != 0:
        # Not in last col
        return i+1

def above(i, width, height):
    if i-width >= 0:
        # not top row
        return i-width

def below(i, width, height):
    if i+width < width*height:
        # not bottom row
        return i+width

def top_left(i, width, height):
    top = above(i, width, height)
    if top is not None:
        return left(top, width, height)

def top_right(i, width, height):
    top = above(i, width, height)
    if top is not None:
        return right(top, width, height)

def bottom_left(i, width, height):
    bottom = below(i, width, height)
    if bottom is not None:
        return left(bottom, width, height)

def bottom_right(i, width, height):
    bottom = below(i, width, height)
    if bottom is not None:
        return right(bottom, width, height)

def get_neighbours(i, width, height):
    functions = [top_left, above, top_right, right, bottom_right, below, bottom_left, left]
    neighbours = [f(i, width, height) for f in functions]
    return [n for n in neighbours if n is not None]

def get_board():
    tiles = list(pyautogui.locateAllOnScreen(TILES[None]))
    tiles = sorted(tiles, key=lambda x: (x[1], x[0]))
    height = sum(1 for i in tiles if i[0]==tiles[0][0])
    width = sum(1 for i in tiles if i[1]==tiles[0][1])
    board = {i: {'location': tile, 'neighbours': get_neighbours(i, width, height), 'value': None} for i, tile in enumerate(tiles)}
    return board

def read_tile_value(screen, tile):
    x, y, w, h = tile['location']
    im = screen.crop((x, y, x+w, y+h))
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
    tile = board[tile_index]
    x, y, w, h = tile['location']
    pyautogui.moveTo(x+w/2, y+h/2)
    pyautogui.click()
    return read_full_board(board)

def is_evaluable(tile_index, board):
    tile = board[tile_index]
    is_clicked = tile['value'] is not None
    is_not_mine = tile['value'] is not 'mine'
    has_unclicked_neighbour = None in [board[t]['value'] for t in tile['neighbours']]
    return is_clicked and has_unclicked_neighbour and is_not_mine

def evaluate(tile_index, board):
    tile = board[tile_index]
    value = tile['value']
    unclicked = [t for t in tile['neighbours'] if board[t]['value'] is None]
    mines = len([t for t in tile['neighbours'] if board[t]['value'] == 'mine'])
    if value == mines:
       for t in unclicked:
           board = click_tile_and_read(t, board)
    if value-mines == len(unclicked):
       for t in unclicked:
           flag_tile(t, board)
           board[t]['value'] = 'mine'
    return board

def flag_tile(tile_index, board):
    tile = board[tile_index]
    x, y, w, h = tile['location']
    pyautogui.moveTo(x+w/2, y+h/2)
    pyautogui.press('space')

def print_board(board):
    tiles = [board[t]['location'] for t in board]
    height = sum(1 for i in tiles if i[0]==tiles[0][0])
    width = sum(1 for i in tiles if i[1]==tiles[0][1])
    for t in board:
        print(t, end=' ')
        print(board[t]['value'])
        if t+1 % width == 0:
            print()

def print_tile(tile, board):
    print(tile)
    for n in tile['neighbours']:
        print(board[n]['value'], end=' ')

if __name__ == '__main__':
    board = get_board()
    # pick a random tile and start the game
    tile = random.choice(list(board.keys()))
    board = click_tile_and_read(tile, board)
    while True:
        start_board = board
        # generate a list of all the tiles that should be evaluated
        evaluable = [tile for tile in board if is_evaluable(tile, board)]
        for tile in evaluable:
            board = evaluate(tile, board)
        if len(evaluable) == 0: 
            print('winner winner chicken dinner')
            break

