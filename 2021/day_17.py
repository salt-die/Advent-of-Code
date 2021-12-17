from itertools import product, starmap
from math import inf

import aoc_helper

XMIN, XMAX, YMIN, YMAX = aoc_helper.utils.extract_ints(aoc_helper.day(17))

def integrate(dx, dy):
    x = y = 0
    max_y = -inf

    while not (
        y < YMIN and dy <= 0
        or dx >= 0 and x > XMAX
        or dx <= 0 and x < XMIN
        or dx == 0 and not (XMIN <= x <= XMAX)
    ):
        x += dx
        y += dy

        dx -= 1 if dx > 0 else -1 if dx < 0 else 0
        dy -= 1

        max_y = max(y, max_y)

        if XMIN <= x <= XMAX and YMIN <= y <= YMAX:
            return True

    return False

def part_one():
    return YMIN * (YMIN + 1) // 2

def part_two():
    LEAST_DX = int((2 * XMIN)**.5)  # Solve: x * (x + 1) / 2 == XMIN => x ~~ (2 * XMIN)**.5
    RECT = product(range(LEAST_DX, XMAX + 1), range(YMIN, abs(YMIN)))

    return sum(starmap(integrate, RECT))

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
