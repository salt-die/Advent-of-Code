from itertools import combinations, starmap

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints

DATA = [
    list(extract_ints(line)) for line in aoc_lube.fetch(year=2023, day=24).splitlines()
]


def valid_intersection(a, b):
    ax, ay, _, adx, ady, _ = a
    bx, by, _, bdx, bdy, _ = b
    ax0 = ax + adx
    ay0 = ay + ady
    bx0 = bx + bdx
    by0 = by + bdy

    denom = (ax - ax0) * (by - by0) - (ay - ay0) * (bx - bx0)
    if denom == 0:
        return False

    det1 = ax * ay0 - ay * ax0
    det2 = bx * by0 - by * bx0
    px = (det1 * (bx - bx0) - det2 * (ax - ax0)) / denom
    py = (det1 * (by - by0) - det2 * (ay - ay0)) / denom
    return (
        200000000000000 <= px <= 400000000000000
        and 200000000000000 <= py <= 400000000000000
        and (px - ax) * adx > 0
        and (py - ay) * ady > 0
        and (px - bx) * bdx > 0
        and (py - by) * bdy > 0
    )


def part_one():
    return sum(starmap(valid_intersection, combinations(DATA, 2)))


def skew(arr3d):
    return np.cross(np.eye(3), arr3d)


def part_two():
    (xp, xv), (yp, yv), (zp, zv) = [
        (np.array(hailstone[:3]), np.array(hailstone[3:])) for hailstone in DATA[:3]
    ]
    unknowns = np.append(
        np.cross(-xp, xv) + np.cross(yp, yv),
        np.cross(-xp, xv) + np.cross(zp, zv),
    )
    m = np.block([[skew(xv - yv), skew(xp - yp)], [skew(xv - zv), skew(xp - zp)]])
    return round(np.linalg.solve(m, unknowns)[:3].sum())


aoc_lube.submit(year=2023, day=24, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=24, part=2, solution=part_two)
