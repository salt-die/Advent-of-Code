from heapq import nlargest
from itertools import combinations, count
from math import dist, prod

import aoc_lube
from aoc_lube.utils import UnionFind, chunk, extract_ints

RAW = list(chunk(extract_ints(aoc_lube.fetch(year=2025, day=8)), 3))
UF = UnionFind(RAW)
DISTANCES = sorted((dist(a, b), a, b) for a, b in combinations(RAW, 2))


def part_one():
    for i in range(1000):
        _, a, b = DISTANCES[i]
        UF.merge(a, b)
    return prod(nlargest(3, (len(component) for component in UF.components)))


def part_two():
    for i in count():
        _, a, b = DISTANCES[i]
        UF.merge(a, b)
        if len(UF.components) == 1:
            return a[0] * b[0]


aoc_lube.submit(year=2025, day=8, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=8, part=2, solution=part_two)
