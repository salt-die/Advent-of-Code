import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints

CLAIMS = [
    tuple(extract_ints(line)) for line in aoc_lube.fetch(year=2018, day=3).splitlines()
]


def parse_raw():
    claims = np.zeros((1000, 1000), int)
    for _, x, y, w, h in CLAIMS:
        claims[y : y + h, x : x + w] += 1
    return claims


DATA = parse_raw()


def part_one():
    return (DATA > 1).sum()


def part_two():
    for claim, x, y, w, h in CLAIMS:
        if (DATA[y : y + h, x : x + w] == 1).all():
            return claim


aoc_lube.submit(year=2018, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2018, day=3, part=2, solution=part_two)


# Alternatively, using regions:
# from batgrl.geometry import Region


# def parse_raw():
#     unions = Region()
#     intersections = Region()
#     for _, x, y, w, h in CLAIMS:
#         r = Region.from_rect((y, x), (h, w))
#         intersections |= r & unions
#         unions |= r
#     return intersections


# def part_one():
#     return sum(h * w for _, (h, w) in DATA.rects())


# def part_two():
#     for claim, x, y, w, h in CLAIMS:
#         r = Region.from_rect((y, x), (h, w))
#         if not DATA & r:
#             return claim
