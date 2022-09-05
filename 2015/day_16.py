import re
from operator import lt, gt, eq

import aoc_helper

RE = r"Sue \d+: (.*): (.*), (.*): (.*), (.*): (.*)"
SUES = [
    {a: int(i), b: int(j), c: int(k)}
    for a, i, b, j, c, k in re.findall(RE, aoc_helper.day(16))
]
MFCSAM = dict(
    children=3,
    cats=7,
    samoyeds=2,
    pomeranians=3,
    akitas=0,
    vizslas=0,
    goldfish=5,
    trees=3,
    cars=2,
    perfumes=1,
)

def part_one():
    for i, sue in enumerate(SUES, start=1):
        if all(v == MFCSAM[k] for k, v in sue.items()):
            return i

def part_two():
    ops = dict(cats=gt, trees=gt, pomeranians=lt, goldfish=lt)
    for i, sue in enumerate(SUES, start=1):
        if all(ops.get(k, eq)(v, MFCSAM[k]) for k, v in sue.items()):
            return i

aoc_helper.submit(16, part_one)
aoc_helper.submit(16, part_two)
