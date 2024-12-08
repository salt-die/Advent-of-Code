from math import log10

import aoc_lube
from aoc_lube.utils import extract_ints

DATA = [
    list(extract_ints(line)) for line in aoc_lube.fetch(year=2024, day=7).splitlines()
]


def endswith(a, b):
    return a % (10 ** (int(log10(b)) + 1)) == b


def unconcat(a, b):
    return a // (10 ** (int(log10(b)) + 1))


def solve(target, operands, part):
    *operands, operand = operands
    if not operands:
        return operand == target
    if (
        part == 2
        and endswith(target, operand)
        and solve(unconcat(target, operand), operands, part)
    ):
        return True
    if target % operand == 0 and solve(target // operand, operands, part):
        return True
    return solve(target - operand, operands, part)


def part_one():
    return sum(target for target, *operands in DATA if solve(target, operands, 1))


def part_two():
    return sum(target for target, *operands in DATA if solve(target, operands, 2))


aoc_lube.submit(year=2024, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=7, part=2, solution=part_two)
