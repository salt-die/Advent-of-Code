import numpy as np

import aoc_helper

GRID = np.array(list(map(list, aoc_helper.day(25).splitlines())))
EMPTY, EAST, SOUTH = ".>v"

def step(universe):
    # move east
    where_east = universe == EAST
    where_empty = universe == EMPTY

    universe = np.where(
        where_east & np.roll(where_empty, -1, 1),
        EMPTY,
        np.where(
            where_empty & np.roll(where_east, 1, 1),
            EAST,
            universe,
        ),
    )

    # move south
    where_south = universe == SOUTH
    where_empty = universe == EMPTY

    universe = np.where(
        where_south & np.roll(where_empty, -1, 0),
        EMPTY,
        np.where(
            where_empty & np.roll(where_south, 1, 0),
            SOUTH,
            universe,
        ),
    )

    return universe

def part_one():
    universe = GRID

    i = 1
    while (universe != (universe := step(universe))).any():
        i += 1

    return i

aoc_helper.submit(25, part_one)
