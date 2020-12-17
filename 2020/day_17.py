import aoc_helper
import numpy as np
from scipy.signal import convolve

raw = aoc_helper.day(17)
data = np.array([[char=="#" for char in line] for line in raw.splitlines()])

def convolve_dimension_(n):
    KERNEL = np.ones(tuple(3 for _ in range(n)), dtype=int)
    KERNEL[tuple(1 for _ in range(n))] = 0

    universe = np.zeros((*(1 for _ in range(n - 2)), *data.shape), dtype=int)
    universe[...,:] = data

    for _ in range(6):
        neighbors = convolve(universe, KERNEL)
        universe = np.where((neighbors == 3) | (np.pad(universe, 1) & (neighbors==2)), 1, 0)
    return universe.sum()

def part_one():
    return convolve_dimension_(3)

def part_two():
    return convolve_dimension_(4)

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
