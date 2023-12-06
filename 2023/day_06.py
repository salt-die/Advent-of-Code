import re
from math import prod

import aoc_lube
from numpy import diff, roots

DATA = re.findall(r"\d+", aoc_lube.fetch(year=2023, day=6))
TIMES = map(int, DATA[:4])
DISTANCES = map(int, DATA[4:])
TIME = int("".join(DATA[:4]))
DISTANCE = int("".join(DATA[4:]))


def n_ways(time, distance):
    return diff(roots([1, time, distance]).astype(int)).item()


def part_one():
    return prod(map(n_ways, TIMES, DISTANCES))


def part_two():
    return n_ways(TIME, DISTANCE)


print(part_one(), part_two())
aoc_lube.submit(year=2023, day=6, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=6, part=2, solution=part_two)
