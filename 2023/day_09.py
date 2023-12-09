import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints

DATA = [
    np.fromiter(extract_ints(line), int)
    for line in aoc_lube.fetch(year=2023, day=9).splitlines()
]


def extrapolate(data):
    return sum(np.diff(data, n=i)[-1] for i in range(len(data)))


def part_one():
    return sum(extrapolate(datum) for datum in DATA)


def part_two():
    return sum(extrapolate(datum[::-1]) for datum in DATA)


aoc_lube.submit(year=2023, day=9, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=9, part=2, solution=part_two)
