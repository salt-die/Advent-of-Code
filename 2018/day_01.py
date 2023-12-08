from itertools import cycle

import aoc_lube
from aoc_lube.utils import extract_ints

FREQUENCIES = list(extract_ints(aoc_lube.fetch(year=2018, day=1)))


def part_one():
    return sum(FREQUENCIES)


def part_two():
    total = 0
    seen = {total}
    for frequency in cycle(FREQUENCIES):
        total += frequency
        if total in seen:
            return total
        seen.add(total)


aoc_lube.submit(year=2018, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2018, day=1, part=2, solution=part_two)
