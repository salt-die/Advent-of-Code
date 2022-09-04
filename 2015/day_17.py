import numpy as np

import aoc_helper
from aoc_helper.utils import extract_ints

def containerize():
    containers = np.array(sorted(extract_ints(aoc_helper.day(17))))
    used_containers = np.zeros_like(containers, dtype=bool)

    def _backtracker(i):
        for j in range(i, len(containers)):
            used_containers[j] = True

            amount = containers @ used_containers
            if amount < 150:
                yield from _backtracker(j + 1)
            elif amount == 150:
                yield used_containers.sum()

            used_containers[j] = False

            if amount >= 150:
                break

    yield from _backtracker(0)

NCONTAINERS_USED = list(containerize())

def part_one():
    return len(NCONTAINERS_USED)

def part_two():
    return NCONTAINERS_USED.count(min(NCONTAINERS_USED))

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
