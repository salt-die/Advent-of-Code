from collections import Counter
from itertools import combinations

import aoc_lube

DATA = aoc_lube.fetch(year=2018, day=2).splitlines()


def part_one():
    counters = [Counter(line) for line in DATA]
    twos = sum(2 in counter.values() for counter in counters)
    threes = sum(3 in counter.values() for counter in counters)
    return twos * threes


def part_two():
    for a, b in combinations(DATA, 2):
        matching = [r for r, s in zip(a, b) if r == s]
        if len(matching) == len(a) - 1:
            return "".join(matching)


aoc_lube.submit(year=2018, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2018, day=2, part=2, solution=part_two)
