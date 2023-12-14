import aoc_lube
import numpy as np

GRID = np.array([list(line) for line in aoc_lube.fetch(2023, 14).splitlines()])


def roll(grids=(GRID, GRID.T, GRID[::-1], GRID.T[::-1])):
    for grid in grids:
        for y, x in np.argwhere(grid == "O"):
            grid[y, x] = "."
            while 0 < y and grid[y - 1, x] == ".":
                y -= 1
            grid[y, x] = "O"


def weight():
    ys, _ = np.nonzero(GRID[::-1] == "O")
    return (ys + 1).sum()


def part_one():
    roll([GRID])
    return weight()


def part_two():
    hashes = {}

    while True:
        bytes = GRID.tobytes()
        if bytes in hashes:
            break
        hashes[bytes] = len(hashes)
        roll()

    start = hashes[bytes]
    cycle_length = len(hashes) - start
    for _ in range((1_000_000_000 - start) % cycle_length):
        roll()

    return weight()


aoc_lube.submit(year=2023, day=14, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=14, part=2, solution=part_two)
