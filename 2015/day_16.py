import re

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
    for i, sue in enumerate(SUES, start=1):
        for k, v in sue.items():
            match k:
                case "cats" | "trees":
                    cond = v > MFCSAM[k]
                case "pomeranians" | "goldfish":
                    cond = v < MFCSAM[k]
                case _:
                    cond = v == MFCSAM[k]
            if not cond:
                break
        else:
            return i

aoc_helper.submit(16, part_one)
aoc_helper.submit(16, part_two)
