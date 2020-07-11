from PIL import Image
import os
import sys
import time
from colorama import Back as b
from colorama import Style

# Cell types
EMPTY = 0
CONDUCTOR = 1
EHEAD = 2
ETAIL = 3

# Value to cell type
CELL_TO_COLOR = {
    CONDUCTOR: b.YELLOW,
    EHEAD: b.LIGHTBLUE_EX,
    ETAIL: b.RED,
    EMPTY: b.BLACK
}

# Cell colors
EMPTY_C = (0, 0, 0)
CONDUCTOR_C = (255, 255, 0)
EHEAD_C = (0, 0, 255)
ETAIL_C = (255, 0, 0)

# Board size
WIDTH = 90
HEIGHT = 50

# The board will be stored in a list of integers, having each integer be EMPTY, EHEAD, or ETAIL or CONDUCTOR.
# The X and Y of a cell will be taken with the location function
# The cell is going to be calculated in the calc_cell function, which returns the next cell type


def get_pixels(path: str) -> list:
    img = Image.open(path)
    if tuple(img.size) == (WIDTH, HEIGHT):
        pixels = []
        raw = img.getdata()
        for rgb in raw:
            # TODO: Get the pixels
            if rgb == EMPTY_C:
                pixels.append(EMPTY)
            elif rgb == CONDUCTOR_C:
                pixels.append(CONDUCTOR)
            elif rgb == EHEAD_C:
                pixels.append(EHEAD)
            elif rgb == ETAIL_C:
                pixels.append(ETAIL)
            else:
                print(rgb)
                raise ValueError
        return pixels
    raise ValueError


def location(x: int, y: int) -> int:
    return y * WIDTH + x


def get_value(board, x: int, y: int) -> int:
    return board[location(x, y)]


def set_value(board, x: int, y: int, new: int) -> None:
    board[location(x, y)] = new


def valid(coor, dim):
    return coor >= 0 and coor <= WIDTH-1 and coor <= HEIGHT-1


def get_x_neigh(board, x: int, y: int) -> int:
    ng = 0
    # Left
    if x > 0 and valid(y, HEIGHT):
        if get_value(board, x-1, y) == EHEAD:
            ng += 1
    # Right
    if x < WIDTH-1 and valid(y, HEIGHT):
        if get_value(board, x+1, y) == EHEAD:
            ng += 1
    return ng


def get_y_neigh(board, x: int, y: int) -> int:
    ng = 0
    # Above
    if y > 0 and valid(x, WIDTH):
        if get_value(board, x, y-1) == EHEAD:
            ng += 1
    # Below
    if y < HEIGHT-1 and valid(x, WIDTH):
        if get_value(board, x, y+1) == EHEAD:
            ng += 1
    return ng


def get_neigh(board, x: int, y: int) -> int:
    ng = 0
    # Horizontal
    ng += get_x_neigh(board, x, y)
    # print("Horizontal:", get_x_neigh(board, x, y))
    # Vertical
    ng += get_y_neigh(board, x, y)
    # print("Vertical:", get_y_neigh(board, x, y))
    # Diagonal - Top
    ng += get_x_neigh(board, x, y-1)
    # print("Diagonal - Top:", get_x_neigh(board, x, y-1))
    # Diagonal - Bottom
    ng += get_x_neigh(board, x, y+1)
    # print("Diagonal - Bottom:", get_x_neigh(board, x, y+1))
    return ng


def calc_cell(board: list, x: int, y: int) -> int:
    ct = get_value(board, x, y)
    if ct == EMPTY:
        # Does nothing
        return EMPTY
    elif ct == EHEAD:
        # Turns into tail
        return ETAIL
    elif ct == ETAIL:
        # Turns into conductor
        return CONDUCTOR
    elif ct == CONDUCTOR:
        # Turns into head if 1 or 2 neighbours are heads
        if get_neigh(board, x, y) == 1 or get_neigh(board, x, y) == 2:
            return EHEAD
        else:
            return CONDUCTOR
    else:
        raise ValueError


def wireworld(name):
    board = get_pixels(name + ".png")
    try:
        while True:
            x = 0
            y = 0
            # new_pixels is used to append each pixel after it has been updated. Used
            # so you can update each pixel "at the same time", as per Conway's Game of Life
            # rules.
            new_board = []
            # Calculate each cell's next state and add changes to the new_board list
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    next_state = calc_cell(board, x, y)
                    new_board.append(next_state)
            # Update board
            board = new_board[:]
            # Print board
            screen = ""
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    val = get_value(board, x, y)
                    screen += CELL_TO_COLOR[val]
                    screen += f"  "
                    # Reset colors every cell
                    screen += Style.RESET_ALL
                screen += "\n"
            # Print screen, used in favor of printing each cell individually, which causes stuttering as
            # the lower cells take longer to be printed
            os.system('clear')
            print(screen)
            time.sleep(0.4)
    except KeyboardInterrupt:
        # If CTRL+C is pressed, exit gracefully, instead of throwing an exception
        os.system('clear')
        sys.exit(0)


wireworld("gates")
