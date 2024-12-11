from functools import cache

import aoc_lube
from aoc_lube.utils import extract_ints, ndigits

STONES = list(extract_ints(aoc_lube.fetch(year=2024, day=11)))


@cache
def blink(stone, n):
    if n == 0:
        return 1

    n -= 1
    if stone == 0:
        return blink(1, n)

    m, r = divmod(ndigits(stone), 2)
    if r == 0:
        a, b = divmod(stone, 10**m)
        return blink(a, n) + blink(b, n)

    return blink(stone * 2024, n)


def part_one():
    return sum(blink(stone, 25) for stone in STONES)


def part_two():
    return sum(blink(stone, 75) for stone in STONES)


aoc_lube.submit(year=2024, day=11, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=11, part=2, solution=part_two)
