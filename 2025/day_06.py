from math import prod

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints, sliding_window

RAW = aoc_lube.fetch(year=2025, day=6)
*NUMBERS, _last = RAW.splitlines()
OPERATORS = _last.split()


def part_one():
    data = np.array([list(extract_ints(row)) for row in NUMBERS])
    return sum(
        np.prod(column) if op == "*" else column.sum()
        for op, column in zip(OPERATORS, data.T)
    )


def solve(problem):
    n = [int("".join(col)) for col in problem[:-1].T]
    return sum(n) if problem[-1, 0] == "+" else prod(n)


def part_two():
    data = np.array([list(row) for row in (RAW + "  ").splitlines()])
    splits = [-1, *np.flatnonzero(np.all(data == " ", axis=0)), None]
    return sum(solve(data[:, a + 1 : b]) for a, b in sliding_window(splits, 2))


aoc_lube.submit(year=2025, day=6, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=6, part=2, solution=part_two)
