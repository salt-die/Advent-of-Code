from itertools import count

import numpy as np
from scipy.ndimage import convolve

import aoc_helper

OCTOPI = aoc_helper.utils.int_grid(aoc_helper.day(11))

KERNEL = np.ones((3, 3), dtype=int)

def step(octos):
    octos += 1

    flashed = np.zeros_like(octos, dtype=bool)
    while (flashing := ((octos > 9) & ~flashed)).any():
        octos += convolve(flashing.astype(int), KERNEL, mode="constant")
        flashed |= flashing

    octos[flashed] = 0
    return flashed.sum()

def part_one():
    octos = OCTOPI.copy()
    return sum(step(octos) for _ in range(100))

def part_two():
    octos = OCTOPI.copy()

    for i in count():
        if (octos == 0).all():
            return i

        step(octos)

aoc_helper.submit(11, part_one)
aoc_helper.submit(11, part_two)
print(part_one(), part_two())