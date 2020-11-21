import pyautogui
import math
import copy
import time
import random
from generate_paths import generate_paths

TOP_LEFT = (797, 544) # x = 797, y = 544 is the center of the top left cell
CELL_OFFSET = 102
INTERVAL = 0.15 # time interval for cursor to move from one cell to another (smaller = faster)

board_letters = [l for l in input("Enter letters: ")]
# board_letters = [l for l in ""]
valid_paths = generate_paths(board_letters)

for path in valid_paths:
    # each iteration/path represents a word found
    start_cell = path[0] # in the form of (row_num, col_num)
    # move cursor to starting cell: x = 797 + col_num * offset, y = 797 + row_num * offset and hold mouse
    pyautogui.moveTo(TOP_LEFT[0] + (start_cell[1] * CELL_OFFSET), TOP_LEFT[1] + (start_cell[0] * CELL_OFFSET))
    pyautogui.mouseDown()
    for cell in path[1:]:
        time.sleep(INTERVAL)
        # move cursor to next cell: x = 797 + col_num * offset, y = 797 + row_num * offset
        pyautogui.moveTo(TOP_LEFT[0] + (cell[1] * CELL_OFFSET), TOP_LEFT[1] + (cell[0] * CELL_OFFSET))
    # release mouse, finish word
    pyautogui.mouseUp()