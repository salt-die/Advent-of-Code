from itertools import count

import aoc_lube
from aoc_lube.utils import Deltas
import numpy as np

def parse_raw():
    blizzards = np.zeros((4, 35, 100), dtype=bool)
    for y, line in enumerate(aoc_lube.fetch(year=2022, day=24).splitlines()[1: -1]):
        for x, c in enumerate(line[1: -1]):
            if c != ".":
                blizzards["v>^<".find(c), y, x] = True
    return blizzards

BLIZZARDS = parse_raw()

def move(a, b):
    positions = {a}

    for steps in count(1):
        for i, face in enumerate(BLIZZARDS):
            BLIZZARDS[i] = np.roll(face, (-1)**(i>>1), i & 1)
        blizzards = BLIZZARDS.any(axis=0)

        if b in positions:
            return steps

        positions = {
            (ny, nx)
            for y, x in positions
            for dy, dx in Deltas.FIVE
            if 0 <= (ny := y + dy) < 35
            if 0 <= (nx := x + dx) < 100
            if not blizzards[ny, nx]
        }

        if steps < 5:  # Assume we don't wait too long at start
            positions.add(a)

def part_one():
    return move((-1, 0), (34, 99))

def part_two():
    return move((-1, 0), (34, 99)) + move((35, 99), (0, 0)) + move((-1, 0), (34, 99))

aoc_lube.submit(year=2022, day=24, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=24, part=2, solution=part_two)
