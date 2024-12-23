from itertools import combinations
from math import prod

import aoc_lube
from aoc_lube.utils import extract_ints

PACKAGES = list(extract_ints(aoc_lube.fetch(year=2015, day=24)))


def min_distribution(n):
    target = sum(PACKAGES) // n
    for i in range(1, len(PACKAGES)):
        good = [prod(x) for x in combinations(PACKAGES, i) if sum(x) == target]
        if good:
            return min(good)


def part_one():
    return min_distribution(3)


def part_two():
    return min_distribution(4)


aoc_lube.submit(year=2015, day=24, part=1, solution=part_one)
aoc_lube.submit(year=2015, day=24, part=2, solution=part_two)
