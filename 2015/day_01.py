from itertools import accumulate

import aoc_helper

RAW = aoc_helper.day(1)
DATA = tuple(accumulate(1 if c == "(" else -1 for c in RAW))

def part_one():
    return DATA[-1]

def part_two():
    return DATA.index(-1) + 1

aoc_helper.submit(1, part_one)
aoc_helper.submit(1, part_two)
