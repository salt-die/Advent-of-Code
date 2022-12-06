import aoc_lube
from aoc_lube.utils import sliding_window

RAW = aoc_lube.fetch(year=2022, day=6)

def distinct_n(n):
    for i, a in enumerate(sliding_window(RAW, n), start=n):
        if len(set(a)) == n:
            return i

def part_one():
    return distinct_n(4)

def part_two():
    return distinct_n(14)

aoc_lube.submit(year=2022, day=6, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=6, part=2, solution=part_two)
