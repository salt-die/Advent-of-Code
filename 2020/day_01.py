import aoc_helper
from itertools import combinations

raw = aoc_helper.day(1)

def parse_raw():
    return [int(line) for line in raw.splitlines()]

data = parse_raw()

def part_one():
    for a, b in combinations(data, 2):
        if a + b == 2020:
            return a * b

def part_two():
    for a, b, c in combinations(data, 3):
        if a + b + c == 2020:
            return a * b * c

aoc_helper.submit(day=1, solv_func=part_one)
aoc_helper.submit(day=1, solv_func=part_two)
