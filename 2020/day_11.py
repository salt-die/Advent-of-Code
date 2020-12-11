from itertools import product, count
from functools import partial

import aoc_helper
import numpy as np
from scipy.ndimage import convolve

raw = aoc_helper.day(11)
FLOOR, EMPTY, OCCUPIED = -1, 0, 1

def parse_raw():
    trans = {".": FLOOR, "L": EMPTY}
    return np.array([[trans[char] for char in line] for line in raw.splitlines()])

data = parse_raw()
floor, no_floor = data == FLOOR, data != FLOOR
h, w = data.shape

def part_one():
    KERNEL = [[1, 1, 1],
              [1, 0, 1],
              [1, 1, 1]]
    last = None
    seats = data

    while (as_bytes := seats.tobytes()) != last:
        last = as_bytes
        neighbors = convolve(np.where(floor, 0, seats), KERNEL, mode="constant")
        seats = np.where(floor, FLOOR, np.where(neighbors >= 4, EMPTY, np.where(neighbors == 0, OCCUPIED, seats)))

    return (seats == OCCUPIED).sum()

@partial(np.vectorize, excluded=[2])
def seen(y, x, seats):
    total = 0
    for y_step, x_step in product((-1, 0, 1), repeat=2):
        if y_step == x_step == 0:
            continue

        for i in count(1):
            cell_y, cell_x = y + i * y_step, x + i * x_step
            if cell_y not in range(0, h) or cell_x not in range(0, w):  # Out-of-bounds
                break
            if (cell := seats[cell_y, cell_x]) != FLOOR:
                total += cell
                break

        if total == 5:
            return total

    return total

def part_two():
    last = None
    seats = neighbors = data.copy()
    ys, xs = np.mgrid[:h, :w]
    ys, xs = ys[no_floor], xs[no_floor]
    while (as_bytes := seats.tobytes()) != last:
        last = as_bytes
        neighbors[no_floor] = seen(ys, xs, seats)
        seats = np.where(neighbors >= 5, EMPTY, np.where(neighbors == 0, OCCUPIED, seats))

    return (seats == OCCUPIED).sum()

aoc_helper.submit(11, part_one)
aoc_helper.submit(11, part_two)
