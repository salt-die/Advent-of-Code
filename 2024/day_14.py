from itertools import count

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2024, day=14)), int).reshape(-1, 2)
POS = DATA[::2]
VEL = DATA[1::2]
DIM = np.array([101, 103])


def part_one():
    quads = np.zeros(4, int)
    for pos, vel in zip(POS, VEL):
        new_pos = (pos + 100 * vel) % DIM
        if (new_pos != (DIM // 2)).all():
            quads[(new_pos < DIM // 2) @ (2, 1)] += 1
    return quads.prod()


def part_two():
    seen = set()
    for i in count():
        for pos, vel in zip(POS, VEL):
            new_pos = tuple((pos + i * vel) % DIM)
            if new_pos in seen:
                seen.clear()
                break
            seen.add(new_pos)
        else:
            return i


aoc_lube.submit(year=2024, day=14, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=14, part=2, solution=part_two)
