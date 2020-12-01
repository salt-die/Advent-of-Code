import aoc_helper
from itertools import combinations

raw = aoc_helper.day(1)

def parse_raw():
    return set(int(line) for line in raw.splitlines())

data = parse_raw()

def part_one():
    for a in data:
        if (b := (2020 - a)) in data:
            return a * b

def part_two():
    for a, b in combinations(data, 2):
        if (c := (2020 - a - b)) in data:
            return a * b * c

aoc_helper.submit(day=1, solv_func=part_one)
aoc_helper.submit(day=1, solv_func=part_two)
