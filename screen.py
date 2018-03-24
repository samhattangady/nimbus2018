import os
import random
import time

import pyautogui
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
    if top:
        return left(top, width, height)

def top_right(i, width, height):
    top = above(i, width, height)
    if top:
        return right(top, width, height)

def bottom_left(i, width, height):
    bottom = below(i, width, height)
    if bottom:
        return left(bottom, width, height)

def bottom_right(i, width, height):
    bottom = below(i, width, height)
    if bottom:
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

def read_tile_value(tile):
    im = pyautogui.screenshot(region=tile['location'])
    for value in TILES:
        if pyautogui.locate(TILES[value], im):
            tile['value'] = value
            break

def read_full_board(board):
    for tile in board:
        print(tile)
        if board[tile]['value'] is not None:
            # Tile has already been read before
            continue
        read_tile_value(board[tile])
    return board

def click_tile_and_read(tile, board):
    x, y, w, h = tile['location']
    pyautogui.moveTo(x+w/2, y+h/2)
    pyautogui.click()


if __name__ == '__main__':
    board = get_board()
    print('got_board')
    while True:
        board = read_full_board(board)
        print('full')
        print(board[0])
    # board = click_tile_and_read(board)
    # print(board)


