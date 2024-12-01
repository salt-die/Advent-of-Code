from collections import Counter

import aoc_lube
from aoc_lube.utils import distribute, extract_ints

L, R = distribute(extract_ints(aoc_lube.fetch(year=2024, day=1)), 2)


def part_one():
    return sum(abs(i - j) for i, j in zip(sorted(L), sorted(R)))


def part_two():
    a = Counter(L)
    b = Counter(R)
    return sum(i * a[i] * b[i] for i in a)


aoc_lube.submit(year=2024, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=1, part=2, solution=part_two)
