from itertools import permutations

import aoc_helper
from aoc_helper.utils import pairwise

G = { }
for line in aoc_helper.day(9).splitlines():
    a, _, b, _, distance = line.split()
    G.setdefault(a, {})[b] = G.setdefault(b, {})[a] = int(distance)

COSTS = [sum(G[u][v] for u, v in pairwise(p)) for p in permutations(G)]

def part_one():
    return min(COSTS)

def part_two():
    return max(COSTS)

aoc_helper.submit(9, part_one)
aoc_helper.submit(9, part_two)
