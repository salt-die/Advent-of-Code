import numpy as np

import aoc_helper
from aoc_helper.utils import extract_ints

def containerize():
    containers = np.array(sorted(extract_ints(aoc_helper.day(17))))
    used_containers = np.zeros_like(containers, dtype=bool)
    ncontainers = len(containers)

    def _backtracker(i):
        if (amount := containers @ used_containers) == 150:
            yield used_containers.sum()
        elif amount < 150:
            for container in range(i, ncontainers):
                used_containers[container] = True
                yield from _backtracker(container + 1)
                used_containers[container] = False

    yield from _backtracker(0)

COMBINATIONS = list(containerize())

def part_one():
    return len(COMBINATIONS)

def part_two():
    return COMBINATIONS.count(min(COMBINATIONS))

aoc_helper.submit(17, part_one)
aoc_helper.submit(17, part_two)
