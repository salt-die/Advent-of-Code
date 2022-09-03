import numpy as np

import aoc_helper
from aoc_helper.utils import extract_ints

SPEEDS, RUN_TIMES, REST_TIMES = np.fromiter(
    extract_ints(aoc_helper.day(14)),
    dtype=int,
).reshape(-1, 3).T

def distances(seconds):
    n, remaining = np.divmod(seconds, RUN_TIMES + REST_TIMES)
    return SPEEDS * (RUN_TIMES * n + np.minimum(RUN_TIMES, remaining))

def part_one():
    return distances(2503).max()

def part_two():
    traveled = distances(np.arange(1, 2504)[:, None])
    return (traveled == traveled.max(axis=1)[:, None]).sum(axis=0).max()

aoc_helper.submit(14, part_one)
aoc_helper.submit(14, part_two)
