from heapq import nlargest
from itertools import combinations
from math import dist, prod

import aoc_lube
from aoc_lube.utils import UnionFind, chunk, extract_ints

UF = UnionFind(chunk(extract_ints(aoc_lube.fetch(year=2025, day=8)), 3))
DISTANCES = sorted(combinations(UF.elements(), 2), key=lambda ps: dist(*ps))


def part_one():
    for a, b in DISTANCES[:1000]:
        UF.merge(a, b)
    return prod(nlargest(3, map(len, UF.components)))


def part_two():
    for a, b in DISTANCES:
        UF.merge(a, b)
        if len(UF.components) == 1:
            return a[0] * b[0]


aoc_lube.submit(year=2025, day=8, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=8, part=2, solution=part_two)
