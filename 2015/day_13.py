import re
from itertools import permutations

import aoc_helper
from aoc_helper.utils import pairwise_cycle

RE = r"(.*) would (gain|lose) (.*) happiness units by sitting next to (.*)."

G = {}
for a, sign, happiness, b in re.findall(RE, aoc_helper.day(13)):
    G.setdefault(a, {})[b] = int(happiness) * (1 if sign == "gain" else -1)

def optimal_score():
    return max(
        sum(G[a][b] + G[b][a] for a, b in pairwise_cycle(p))
        for p in permutations(G)
    )

def part_one():
    return optimal_score()

def part_two():
    for scores in G.values():
        scores["salt-die"] = 0

    G["salt-die"] = {name: 0 for name in G}
    return optimal_score()

aoc_helper.submit(13, part_one)
aoc_helper.submit(13, part_two)
