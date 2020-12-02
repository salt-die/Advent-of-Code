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
    # We know that at least two of the numbers must be less than half the target.
    filtered_data = (i for i in data if i < 1010)

    for a, b in combinations(filtered_data, 2):
        if (c := (2020 - a - b)) in data:
            return a * b * c

aoc_helper.submit(day=1, solv_func=part_one)
aoc_helper.submit(day=1, solv_func=part_two)
