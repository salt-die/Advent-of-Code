import aoc_helper
import numpy as np
from scipy.ndimage import convolve

raw = aoc_helper.day(17)
data = np.array([[char=="#" for char in line] for line in raw.splitlines()])

def convolve_dimension_(n):
    KERNEL = np.ones(tuple(3 for _ in range(n)))
    KERNEL[tuple(1 for _ in range(n))] = 0

    universe = np.zeros((*(13 for _ in range(n - 2)), 20, 20), dtype=int)
    universe[tuple(6 for _ in range(n - 2))] = np.pad(data, 6)

    for _ in range(6):
        neighbors = convolve(universe, KERNEL, mode="constant")
        universe = np.where((neighbors == 3) | (universe & (neighbors==2)), 1, 0)
    return universe.sum()

def part_one():
    return convolve_dimension_(3)

def part_two():
    return convolve_dimension_(4)

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
