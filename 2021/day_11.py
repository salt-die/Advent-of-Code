from itertools import count

import numpy as np

import aoc_helper

OCTOPI = aoc_helper.utils.int_grid(aoc_helper.day(11))

KERNEL = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
])

def step(padded_octos):
    octos = padded_octos[1: -1, 1: -1]

    octos += 1
    flashed = np.zeros_like(octos, dtype=bool)
    while ((flashing := octos > 9) != flashed).any():
        new_flashes = np.argwhere(flashing & ~flashed)

        for y, x in new_flashes:
            padded_octos[y: y + 3, x: x + 3] += KERNEL

        flashed |= flashing

    octos[flashed] = 0

    return flashed.sum()

def part_one():
    padded_octos = np.pad(OCTOPI, 1)
    return sum(step(padded_octos) for _ in range(100))

def part_two():
    padded_octos = np.pad(OCTOPI, 1)
    octos = padded_octos[1: -1, 1: -1]

    for i in count():
        if (octos == 0).all():
            return i

        step(padded_octos)

aoc_helper.submit(11, part_one)
aoc_helper.submit(11, part_two)
