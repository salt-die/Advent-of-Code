import aoc_helper
import numpy as np
from scipy.ndimage import convolve

raw = aoc_helper.day(17)
data = np.array([[char=="#" for char in line] for line in raw.splitlines()], dtype=int)

def part_one():
    KERNEL = np.ones((3, 3, 3))
    KERNEL[1, 1, 1] = 0

    universe = np.zeros((13, 20, 20), dtype=int)
    universe[6] = np.pad(data, 6)

    for _ in range(6):
        neighbors = convolve(universe, KERNEL, mode="constant")
        universe = np.where((neighbors == 3) | (universe & (neighbors==2)), 1, 0)
    return universe.sum()

def part_two():
    KERNEL = np.ones((3, 3, 3, 3))
    KERNEL[1, 1, 1, 1] = 0

    universe = np.zeros((13, 13, 20, 20), dtype=int)
    universe[6, 6] = np.pad(data, 6)

    for _ in range(6):
        neighbors = convolve(universe, KERNEL, mode="constant")
        universe = np.where((neighbors == 3) | (universe & (neighbors==2)), 1, 0)
    return universe.sum()

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
