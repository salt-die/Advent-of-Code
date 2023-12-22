from bisect import insort

import aoc_lube
from aoc_lube.utils import extract_ints


def fall(bricks):
    stack, fell = [], 0
    for x1, y1, z1, x2, y2, z2 in bricks:
        h = z2 - z1
        t1 = 1
        for r1, s1, t1, r2, s2, t2 in reversed(stack):
            if not (x2 < r1 or r2 < x1) and not (s2 < y1 or y2 < s1):
                fell += z1 != t2 + 1
                z1 = t2 + 1
                break
        else:
            fell += z1 != t1
            z1 = t1
        insort(stack, [x1, y1, z1, x2, y2, z1 + h], key=lambda brick: brick[5])
    return stack, fell


BRICKS = [
    [*extract_ints(line)] for line in aoc_lube.fetch(year=2023, day=22).splitlines()
]
BRICKS.sort(key=lambda brick: brick[5])
STACK, _ = fall(BRICKS)
N = len(BRICKS)


def part_one():
    return sum(fall(STACK[:i] + STACK[i + 1 :])[1] == 0 for i in range(N))


def part_two():
    return sum(fall(STACK[:i] + STACK[i + 1 :])[1] for i in range(N))


aoc_lube.submit(year=2023, day=22, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=22, part=2, solution=part_two)
