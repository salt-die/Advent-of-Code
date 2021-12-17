from itertools import product
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
            return max_y

    return -inf

def part_one():
    return YMIN * (YMIN + 1) // 2

def part_two():
    return sum(
        1 if integrate(dx, dy) != -inf else 0
        for dx, dy in product(
            range(int((2 * XMIN)**.5), XMAX + 1),   # Solve: x * (x + 1) / 2 == XMIN => x ~~ (2 * XMIN)**.5
            range(YMIN, abs(YMIN)),
        )
    )

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
print(part_two())