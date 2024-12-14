from itertools import count

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2024, day=14)), int).reshape(-1, 2)
POS = DATA[::2]
VEL = DATA[1::2]
DIM = np.array([101, 103])


def part_one():
    pos = (POS + 100 * VEL) % DIM
    not_centered = pos[np.all(pos != DIM // 2, axis=-1)]
    return np.bincount((not_centered < DIM // 2) @ (2, 1)).prod()


def part_two():
    for i in count():
        if np.unique((POS + i * VEL) % DIM, axis=0).shape == POS.shape:
            return i


aoc_lube.submit(year=2024, day=14, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=14, part=2, solution=part_two)
