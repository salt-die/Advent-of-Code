from itertools import combinations

import aoc_lube
import numpy as np


def parse_raw():
    grid = aoc_lube.fetch(year=2023, day=11).splitlines()
    yield np.array([y for y, line in enumerate(grid) for char in line if char == "#"])
    yield np.array([x for x in range(len(grid[0])) for line in grid if line[x] == "#"])


YS, XS = parse_raw()


def expand(axis, n):
    diffs = np.diff(axis, prepend=0) - 1
    diffs[diffs < 0] = 0
    return axis + np.cumsum(diffs) * n


def expand_universe(n):
    return sum(
        abs(a - b)
        for axis in (expand(YS, n), expand(XS, n))
        for a, b in combinations(axis, 2)
    )


def part_one():
    return expand_universe(1)


def part_two():
    return expand_universe(999_999)


aoc_lube.submit(year=2023, day=11, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=11, part=2, solution=part_two)
