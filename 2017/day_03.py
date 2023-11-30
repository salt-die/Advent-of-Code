from collections import defaultdict
from itertools import islice

import aoc_lube
from aoc_lube.utils import GRID_NEIGHBORHOODS, spiral_grid

N = int(aoc_lube.fetch(year=2017, day=3))


def part_one():
    x, y = next(islice(spiral_grid(), N - 1, None))
    return abs(x) + abs(y)


def part_two():
    grid = defaultdict(int)
    spiral = spiral_grid()
    grid[next(spiral)] = 1
    for x, y in spiral:
        grid[x, y] = sum(grid[x + dx, y + dy] for dx, dy in GRID_NEIGHBORHOODS[8])
        if grid[x, y] > N:
            return grid[x, y]


aoc_lube.submit(year=2017, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2017, day=3, part=2, solution=part_two)
