from itertools import product, count

import aoc_helper
from scipy.ndimage import convolve
import numpy as np

raw = aoc_helper.day(11)
FLOOR, EMPTY, OCCUPIED = -1, 0, 1

def parse_raw():
    trans = {".": FLOOR, "L": EMPTY}
    return np.array([[trans[char] for char in line] for line in raw.splitlines()])

seats = parse_raw()
floor = seats == -1
h, w = seats.shape

def part_one():
    KERNEL = [[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]]
    last = None
    data = seats
    while (as_bytes := data.tobytes()) != last:
        last = as_bytes
        neighbors = convolve(np.where(floor, 0, data), KERNEL, mode="constant")
        data = np.where(floor, FLOOR, np.where(neighbors >= 4, EMPTY, np.where(neighbors == 0, OCCUPIED, data)))
    return (data == OCCUPIED).sum()

def check_line(y, x, y_step, x_step, data):
    if y_step == x_step == 0:
        return 0

    for i in count(1):
        cell_y, cell_x = y + i * y_step, x + i * x_step
        if cell_y not in range(0, h) or cell_x not in range(0, w):
            return 0
        if (cell := data[cell_y, cell_x]) != -1:
            return cell

def part_two():
    last = None
    data = seats.copy()
    while (as_bytes := data.tobytes()) != last:
        last = as_bytes
        neighbors = np.zeros_like(data)
        it = np.nditer(data, flags=["multi_index"])
        for seat in it:
            y, x = it.multi_index
            if seat == FLOOR:
                neighbors[y, x] = FLOOR
            else:
                neighbors[y, x] = sum(check_line(y, x, i, j, data) for i, j in product((-1, 1, 0), repeat=2))
        data = np.where(neighbors >= 5, EMPTY, np.where(neighbors == 0, OCCUPIED, data))

    return (data == OCCUPIED).sum()

aoc_helper.submit(11, part_one)
aoc_helper.submit(11, part_two)
