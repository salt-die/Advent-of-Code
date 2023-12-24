from itertools import combinations, starmap

import aoc_lube
from aoc_lube.utils import extract_ints
from sympy import solve_poly_system, symbols

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


def part_two():
    x, y, z, dx, dy, dz, t0, t1, t2 = variables = symbols("x y z dx dy dz t0 t1 t2")
    (
        (x0, y0, z0, dx0, dy0, dz0),
        (x1, y1, z1, dx1, dy1, dz1),
        (x2, y2, z2, dx2, dy2, dz2),
    ) = DATA[:3]
    [(x, y, z, *_)] = solve_poly_system(
        [
            x + dx * t0 - x0 - dx0 * t0,
            y + dy * t0 - y0 - dy0 * t0,
            z + dz * t0 - z0 - dz0 * t0,
            x + dx * t1 - x1 - dx1 * t1,
            y + dy * t1 - y1 - dy1 * t1,
            z + dz * t1 - z1 - dz1 * t1,
            x + dx * t2 - x2 - dx2 * t2,
            y + dy * t2 - y2 - dy2 * t2,
            z + dz * t2 - z2 - dz2 * t2,
        ],
        *variables,
    )
    return x + y + z


aoc_lube.submit(year=2023, day=24, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=24, part=2, solution=part_two)
