import aoc_lube
import numpy as np
from aoc_lube.utils import int_grid

BATTERIES = int_grid(aoc_lube.fetch(year=2025, day=3))


def max_joltage(row, n: int) -> int:
    indices = []
    for i in range(n):
        start = (indices[-1] + 1) if indices else 0
        end = (i - 11) or None
        indices.append(np.argmax(row[start:end]) + start)
    return sum(10**i * row[n] for i, n in enumerate(reversed(indices)))


def part_one():
    return sum(max_joltage(row, 2) for row in BATTERIES)


def part_two():
    return sum(max_joltage(row, 12) for row in BATTERIES)


aoc_lube.submit(year=2025, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=3, part=2, solution=part_two)
