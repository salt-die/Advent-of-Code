from itertools import combinations, pairwise

import aoc_lube
import numpy as np

RAW = aoc_lube.fetch(year=2023, day=11)


def parse_raw():
    universe = RAW.splitlines()
    ys = [y for y, line in enumerate(universe) for char in line if char == "#"]
    xs = [x for line in universe for x, char in enumerate(line) if char == "#"]
    ys.sort()
    xs.sort()
    return np.array(ys, np.int64), np.array(xs, np.int64)


YS, XS = parse_raw()


def _expand(axis, n):
    diffs = np.diff(axis) - 1
    diffs[diffs < 0] = 0
    axis[1:] += np.cumsum(diffs) * n


def expand_universe(n):
    _expand(YS, n)
    _expand(XS, n)
    return sum(abs(a - b) for axis in [YS, XS] for a, b in combinations(axis, 2))


def part_one():
    return expand_universe(1)


def part_two():
    return expand_universe(999_999)


aoc_lube.submit(year=2023, day=11, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=11, part=2, solution=part_two)
