import aoc_lube
import numpy as np
from scipy.ndimage import convolve

RAW = aoc_lube.fetch(year=2025, day=4)
DATA = np.array([[int(c == "@") for c in row] for row in RAW.splitlines()])
KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def part_one():
    neighbors = convolve(DATA, KERNEL, mode="constant")
    return np.logical_and(DATA, neighbors < 4).sum()


def part_two():
    rolls = DATA.copy()

    while True:
        to_remove = np.logical_and(rolls, convolve(rolls, KERNEL, mode="constant") < 4)
        if not to_remove.any():
            return DATA.sum() - rolls.sum()
        rolls -= to_remove


aoc_lube.submit(year=2025, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=4, part=2, solution=part_two)
