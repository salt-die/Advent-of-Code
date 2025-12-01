import aoc_lube
from aoc_lube.utils import extract_ints

ROTATIONS = list(extract_ints(aoc_lube.fetch(year=2025, day=1).replace("L", "-")))


def part_one():
    dial = 50
    zeros = 0
    for n in ROTATIONS:
        dial += n
        zeros += dial % 100 == 0
    return zeros


def part_two():
    dial = 50
    zeros = 0
    for n in ROTATIONS:
        at_zero = dial == 0
        r, dial = divmod(dial + n, 100)
        zeros += abs(r)
        if n < 0:
            zeros += (dial == 0) - at_zero
    return zeros


aoc_lube.submit(year=2025, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=1, part=2, solution=part_two)
