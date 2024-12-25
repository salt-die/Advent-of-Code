from itertools import combinations

import aoc_lube

KEYS = aoc_lube.fetch(year=2024, day=25).split("\n\n")


def fits(key, lock):
    return all(a + b != "##" for a, b in zip(key, lock))


def part_one():
    return sum(fits(a, b) for a, b in combinations(KEYS, r=2))


aoc_lube.submit(year=2024, day=25, part=1, solution=part_one)
