import numpy as np

import aoc_helper

RAW = aoc_helper.day(6)

FISH = np.full(9, 0, dtype=object)

for n in aoc_helper.utils.extract_ints(RAW):
    FISH[n] += 1

def nfish(steps):
    all_fish = FISH.copy()

    for i in range(steps):
        all_fish[(i + 7) % 9] += all_fish[i % 9]

    return all_fish.sum()

def part_one():
    return nfish(80)

def part_two():
    return nfish(256)

aoc_helper.submit(6, part_one)
aoc_helper.submit(6, part_two)

print(part_one(), part_two())