from itertools import starmap

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2024, day=13)), int).reshape(-1, 2)
AS = DATA[::3]
BS = DATA[1::3]
PRIZES = DATA[2::3]


def linear_combination(a, b, x):
    M = np.stack([a, b])
    s = (np.linalg.solve(M.T, x) + 0.5).astype(int)
    return s @ (3, 1) if (s @ M == x).all() else 0


def part_one():
    return sum(starmap(linear_combination, zip(AS, BS, PRIZES)))


def part_two():
    return sum(starmap(linear_combination, zip(AS, BS, PRIZES + 10000000000000)))


aoc_lube.submit(year=2024, day=13, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=13, part=2, solution=part_two)
