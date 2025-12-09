from itertools import combinations

import aoc_lube
from aoc_lube.utils import chunk, extract_ints
from shapely import Polygon

POINTS = list(chunk(extract_ints(aoc_lube.fetch(year=2025, day=9)), 2))


def area(a, b):
    x1, y1 = a
    x2, y2 = b
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def rect(a, b):
    x1, y1 = a
    x2, y2 = b
    return Polygon([a, (x2, y1), b, (x1, y2)])


def part_one():
    return max(area(a, b) for a, b in combinations(POINTS, 2))


def part_two():
    polygon = Polygon(POINTS)
    return max(
        area(a, b) for a, b in combinations(POINTS, 2) if polygon.covers(rect(a, b))
    )


aoc_lube.submit(year=2025, day=9, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=9, part=2, solution=part_two)
