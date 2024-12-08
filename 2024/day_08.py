from itertools import combinations

import aoc_lube
import numpy as np

GRID = np.array([list(line) for line in aoc_lube.fetch(year=2024, day=8).splitlines()])
H, W = GRID.shape
FREQUENCIES = [freq for freq in np.unique(GRID) if freq != "."]


def inbounds(y, x):
    return 0 <= y < H and 0 <= x < W


def mark_podes(y, x, dy, dx, podes, part):
    if part == 1:
        if inbounds(y + dy, x + dx):
            podes[y + dy, x + dx] = 1
        return

    while inbounds(y, x):
        podes[y, x] = 1
        y += dy
        x += dx


def sum_antipodes(part):
    antipodes = np.zeros((H, W), int)
    for freq in FREQUENCIES:
        for a, b in combinations(np.argwhere(GRID == freq), r=2):
            mark_podes(*a, *a - b, antipodes, part)
            mark_podes(*b, *b - a, antipodes, part)
    return antipodes.sum()


def part_one():
    return sum_antipodes(1)


def part_two():
    return sum_antipodes(2)


aoc_lube.submit(year=2024, day=8, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=8, part=2, solution=part_two)
