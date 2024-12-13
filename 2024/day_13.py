import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints
from sympy import solve_linear_system
from sympy.abc import x, y

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2024, day=13)), int).reshape(-1, 2)
AS = DATA[::3]
BS = DATA[1::3]
PRIZES = DATA[2::3]


def linear_combination(A, B, X):
    solution = solve_linear_system(np.hstack((np.stack([A, B]).T, X[:, None])), x, y)
    if solution and solution[x].is_integer and solution[y].is_integer:
        return solution[x] * 3 + solution[y]
    return 0


def part_one():
    return sum(linear_combination(A, B, X) for A, B, X in zip(AS, BS, PRIZES))


def part_two():
    return sum(
        linear_combination(A, B, X) for A, B, X in zip(AS, BS, PRIZES + 10000000000000)
    )


aoc_lube.submit(year=2024, day=13, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=13, part=2, solution=part_two)
