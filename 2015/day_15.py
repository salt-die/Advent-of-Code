import numpy as np

import aoc_helper
from aoc_helper.utils import extract_ints, partitions

INGREDIENTS = np.fromiter(
    extract_ints(aoc_helper.day(15)),
    dtype=int,
).reshape(-1, 5)

PARTITIONS = np.array(list(partitions(100, 4)))
SUBTOTALS = PARTITIONS @ INGREDIENTS
SCORES = np.clip(SUBTOTALS[:, :4], 0, None).prod(axis=1)

def part_one():
    return SCORES.max()

def part_two():
    return SCORES[SUBTOTALS[:, 4] == 500].max()

aoc_helper.submit(15, part_one)
aoc_helper.submit(15, part_two)
