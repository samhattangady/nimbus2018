import os
import random
import time

import pyautogui

def take_screenshot():
    sct = mss()
    sct.shot()

def restart():
    pyautogui.press('f2')

def game_on():
    return bool(pyautogui.locateCenterOnScreen('images/smiley.png'))

def random_unclicked():
    unclicked = list(pyautogui.locateAllOnScreen('images/unclicked.png'))
    tile = random.choice(unclicked)
    pyautogui.moveTo(tile[0]+tile[2]/2 , tile[1]+tile[3]/2)
    pyautogui.click()

def rando():
    restart = pyautogui.locateCenterOnScreen('images/smiley.png')
    if restart:
        x,y = restart
    while True:
        while game_on():
            random_unclicked()
        pyautogui.moveTo(x, y, 1)
        pyautogui.click()

def get_board():
    board = list(pyautogui.locateAllOnScreen('images/unclicked.png'))
    board = sorted(board, key=lambda x: (x[1], x[0]))
    height = sum(1 for i in board if i[0]==board[0][0])
    width = sum(1 for i in board if i[1]==board[0][1])
    board = [[b, 'n'] for b in board]
    grid = [board[i:i+width] for i in range(0, len(board), width)]
    return grid

def read_full_board(board):
    new = []
    for row in board:
        new_row = []
        for tile in row:
            if tile[1] not in ['?', 'n']:
                new_row.append(tile)
                continue
            im = pyautogui.screenshot(region=tile[0])
            if pyautogui.locate('images/unclicked.png', im):
                new_row.append([tile[0], 'n'])
            elif pyautogui.locate('images/zero.png', im):
                new_row.append([tile[0], ' '])
            elif pyautogui.locate('images/one.png', im):
                new_row.append([tile[0], '1'])
            elif pyautogui.locate('images/two.png', im):
                new_row.append([tile[0], '2'])
            else:
                new_row.append([tile[0], '?'])
        new.append(new_row)
    return new

def print_board(board):
    os.system('clear')
    for row in board:
        for tile in row:
            print(tile[1], end = ' ')
        print()

if __name__ == '__main__':
    board = get_board()
    while True:
        board = read_full_board(board)
        print_board(board)

