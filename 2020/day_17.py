import aoc_helper
import numpy as np
from scipy.signal import convolve

raw = aoc_helper.day(17)
data = np.array([[char=="#" for char in line] for line in raw.splitlines()])

def convolve_dimension_(n):
    KERNEL = np.ones((3, ) * n, dtype=np.uint8)
    KERNEL[(1, ) * n] = 0

    universe = data[(None, ) * (n - 2) + (..., )]

    for _ in range(6):
        neighbors = convolve(universe, KERNEL)
        universe = (neighbors == 3) | (np.pad(universe, 1) & (neighbors == 2))
    return universe.sum()

def part_one():
    return convolve_dimension_(3)

def part_two():
    return convolve_dimension_(4)

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
