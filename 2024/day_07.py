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


def solve(equation, part):
    target, *operands = equation

    def _solve(target, index):
        operand = operands[index]
        if index == 0:
            return operand == target
        if (
            part == 2
            and endswith(target, operand)
            and _solve(unconcat(target, operand), index - 1)
        ):
            return True
        if target % operand == 0 and _solve(target // operand, index - 1):
            return True
        return _solve(target - operand, index - 1)

    return target if _solve(target, len(operands) - 1) else 0


def part_one():
    return sum(solve(equation, 1) for equation in DATA)


def part_two():
    return sum(solve(equation, 2) for equation in DATA)


aoc_lube.submit(year=2024, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=7, part=2, solution=part_two)
