from itertools import accumulate

import aoc_helper

RAW = aoc_helper.day(3)

TRANSLATE = {
    "^": 1j,
    "v": -1j,
    ">": 1,
    "<": -1,
}

DATA = [TRANSLATE[c] for c in RAW]

def unique_houses(*instructions):
    visited = {0}
    for instruction in instructions:
        visited.update(accumulate(instruction))
    return len(visited)

def part_one():
    return unique_houses(DATA)

def part_two():
    return unique_houses(DATA[::2], DATA[1::2])

aoc_helper.submit(3, part_one)
aoc_helper.submit(3, part_two)
