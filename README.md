# Nimbus2018

The nimbus series of broomsticks is the fastest series of broomsticks 
currently in production. They sweep real fast. Apparently, they even 
sweep mines.

_Nimbus2018_ is a minesweeper bot written to get on the highscore list
on _minesweeperonline_.

## Running

1. Open _minesweeperonline_ on Google Chrome. Change the zoom to 175%
2. Open a terminal window, and ensure that it is not blocking any part of the
minesweeper board.
3. `cd` into `path/to/nimbus2018`
4. Run the command `python3 solve.py`
5. Watch in awe. Cross your fingers and hope you got a solvable board. [In case you are facing an error, you might have to replace the images directory yourself.]
6. Think up a creative name for your high score.
7. Exercise your bragging rights in a resposible manner.

## Notes

Nimbus2018 uses `pyautogui` for reading the screen, and controlling the mouse.

PIL is used for recognising the values on screen.

Nimbus can be used on partially solved boards, in case you are stuck.

Specifics of the development environment. Certain things may need changing
when using any other environment.

1. OS: Kubuntu 17.10
2. Python version: 3.6.3
3. Screen dimensions: 1366 x 768
4. minesweeperonline zoom level on chrome: 175%
