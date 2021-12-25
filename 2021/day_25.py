import numpy as np

import aoc_helper

FLOOR = np.array(list(map(list, aoc_helper.day(25).splitlines())))
EMPTY, EAST, SOUTH = ".>v"

def step():
    moving_east = (FLOOR == EAST) & np.roll(FLOOR == EMPTY, -1, 1)

    FLOOR[moving_east] = EMPTY
    FLOOR[np.roll(moving_east, 1, 1)] = EAST

    moving_south = (FLOOR == SOUTH) & np.roll(FLOOR == EMPTY, -1, 0)

    FLOOR[moving_south] = EMPTY
    FLOOR[np.roll(moving_south, 1, 0)] = SOUTH

    return (moving_east | moving_south).any()

def part_one():
    return sum(iter(step, False)) + 1

aoc_helper.submit(25, part_one)
