from functools import reduce

import aoc_lube
from aoc_lube.utils import extract_ints

import numpy as np
from shapely import LineString, Polygon, union_all, difference

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2022, day=15)), int).reshape(-1, 2, 2)
SENSORS = DATA[:, 0]
DISTANCES = np.linalg.norm(SENSORS - DATA[:, 1], ord=1, axis=1).astype(int)

def part_one():
    xs, ys = SENSORS.T
    widths = DISTANCES - abs(ys - 2_000_000)
    mask = widths > 0
    intervals = [LineString(((x - width, 0), (x + width, 0))) for x, width in zip(xs[mask], widths[mask])]
    return int(union_all(intervals).length)

def part_two():
    MAX = 4_000_000
    diamonds = (Polygon(((x + r, y), (x, y + r), (x - r, y), (x, y - r))) for (x, y), r in zip(SENSORS, DISTANCES))
    beacon = reduce(difference, diamonds, Polygon(((0, 0), (0, MAX), (MAX, MAX), (MAX, 0)))).centroid
    return int(beacon.x * MAX + beacon.y)

aoc_lube.submit(year=2022, day=15, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=15, part=2, solution=part_two)
