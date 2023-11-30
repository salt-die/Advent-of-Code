from itertools import permutations

import aoc_lube
from aoc_lube.utils import extract_ints

SHEET = [
    list(extract_ints(row)) for row in aoc_lube.fetch(year=2017, day=2).splitlines()
]


def part_one():
    return sum(max(row) - min(row) for row in SHEET)


def part_two():
    total = 0
    for row in SHEET:
        for a, b in permutations(row, 2):
            f = a / b
            if f.is_integer():
                total += int(f)
                break
    return total


aoc_lube.submit(year=2017, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2017, day=2, part=2, solution=part_two)
