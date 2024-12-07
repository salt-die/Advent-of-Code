from itertools import product
from math import log10
from operator import add, mul

import aoc_lube
from aoc_lube.utils import extract_ints

DATA = [
    list(extract_ints(line)) for line in aoc_lube.fetch(year=2024, day=7).splitlines()
]


def concat(a, b):
    return int(a * 10 ** (int(log10(b)) + 1) + b)


def solve(equation, operators):
    target, initial, *operands = equation
    for guess in product(operators, repeat=len(operands)):
        result = initial
        for operator, operand in zip(guess, operands):
            result = operator(result, operand)
            if result > target:
                break
        if result == target:
            return target
    return 0


def part_one():
    return sum(solve(equation, (add, mul)) for equation in DATA)


def part_two():
    return sum(solve(equation, (add, mul, concat)) for equation in DATA)


aoc_lube.submit(year=2024, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=7, part=2, solution=part_two)
