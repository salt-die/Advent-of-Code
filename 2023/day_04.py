import aoc_lube
import numpy as np


def parse_raw():
    for line in aoc_lube.fetch(year=2023, day=4).splitlines():
        ints = list(aoc_lube.utils.extract_ints(line))
        yield len(set(ints[1:11]) & set(ints[11:]))


MATCHES = np.fromiter(parse_raw(), int)


def part_one():
    return (2 ** (MATCHES[MATCHES > 0] - 1)).sum()


def part_two():
    copies = np.ones_like(MATCHES)
    for i, matches in enumerate(MATCHES):
        copies[i + 1 : i + 1 + matches] += copies[i]
    return copies.sum()


aoc_lube.submit(year=2023, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=4, part=2, solution=part_two)
