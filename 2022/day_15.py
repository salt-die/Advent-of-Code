from itertools import combinations

import aoc_lube
from aoc_lube.utils import extract_ints

import numpy as np
from shapely import (
    LineString,
    LinearRing,
    MultiPoint,
    Polygon,
    intersection,
    union_all,
)

DATA = np.fromiter(extract_ints(aoc_lube.fetch(year=2022, day=15)), int).reshape(-1, 2, 2)
SENSORS = DATA[:, 0]
XS, YS = SENSORS.T
BEACONS = DATA[:, 1]
DISTANCES = np.linalg.norm(SENSORS - BEACONS, ord=1, axis=1).astype(int)

def part_one():
    row = 2_000_000
    intersection_widths = DISTANCES - abs(YS - row)
    mask = intersection_widths > 0

    intervals = [
        LineString(((x - width, row), (x + width, row)))
        for x, width in zip(XS[mask], intersection_widths[mask])
    ]

    return int(union_all(intervals).length)

def part_two():
    valid_region = Polygon([(0, 0), (4_000_000, 0), (4_000_000, 4_000_000)])

    boundaries = [
        LinearRing((
            (x + r + 1, y),
            (x, y + r + 1),
            (x - r - 1, y),
            (x, y - r - 1),
        ))
        for (x, y), r in zip(SENSORS, DISTANCES)
    ]
    candidates = set()
    for a, b in combinations(boundaries, r=2):
        if isinstance(points := intersection(a, b), MultiPoint):
            for point in points.geoms:
                if (
                    valid_region.contains(point) and
                    point.x.is_integer() and
                    point.y.is_integer()
                ):
                    candidates.add((int(point.x), int(point.y)))

    for candidate in candidates:
        for sensor, d in zip(SENSORS, DISTANCES):
            if np.linalg.norm(sensor - candidate, ord=1) < d:
                break
        else:
            x, y = candidate
            return 4_000_000 * x + y

aoc_lube.submit(year=2022, day=15, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=15, part=2, solution=part_two)
