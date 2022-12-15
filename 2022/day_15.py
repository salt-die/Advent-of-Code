from itertools import combinations

import aoc_lube
from aoc_lube.utils import extract_ints

import numpy as np
from shapely import LineString, LinearRing, MultiPoint, intersection, union_all

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2022, day=15)), int).reshape(-1, 2, 2)
SENSORS = DATA[:, 0]
DISTANCES = np.linalg.norm(SENSORS - DATA[:, 1], ord=1, axis=1).astype(int)

def part_one():
    intersection_widths = DISTANCES - abs(SENSORS[:, 1] - 2_000_000)
    mask = intersection_widths > 0

    intervals = [
        LineString(((x - width, 0), (x + width, 0)))
        for x, width in zip(SENSORS[:, 0][mask], intersection_widths[mask])
    ]

    return int(union_all(intervals).length)

def part_two():
    boundaries = [
        LinearRing(((x + r + 1, y), (x, y + r + 1), (x - r - 1, y), (x, y - r - 1)))
        for (x, y), r in zip(SENSORS, DISTANCES)
    ]  # diamond-boundaries

    candidates = {
        (int(point.x), int(point.y))

        for a, b in combinations(boundaries, r=2)
        if isinstance(points := intersection(a, b), MultiPoint)

        for point in points.geoms
        if 0 <= point.x <= 4_000_000
        if 0 <= point.y <= 4_000_000
        if point.x.is_integer()
        if point.y.is_integer()
    }  # integer boundary intersections within bounds

    for candidate in candidates:
        for sensor, d in zip(SENSORS, DISTANCES):
            if np.linalg.norm(sensor - candidate, ord=1) < d:
                break
        else:  # candidate is outside of all diamond-boundaries
            x, y = candidate
            return 4_000_000 * x + y

aoc_lube.submit(year=2022, day=15, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=15, part=2, solution=part_two)
