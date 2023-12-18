import aoc_lube
import shapely
from aoc_lube.utils import distribute


def parse_raw():
    to_dydx = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    to_dydx |= {d: v for d, v in zip("3120", to_dydx.values())}
    for line in aoc_lube.fetch(2023, 18).splitlines():
        dir, n, color = line.split()
        yield to_dydx[dir], int(n)
        yield to_dydx[color[-2]], int(color[2:-2], 16)


def points(data):
    y = x = 0
    for (dy, dx), n in data:
        y += dy * n
        x += dx * n
        yield y, x


PART1, PART2 = map(points, distribute(parse_raw(), 2))


def polyarea(points):
    poly = shapely.Polygon(points)
    return int(poly.area + poly.length / 2 + 1)


aoc_lube.submit(year=2023, day=18, part=1, solution=lambda: polyarea(PART1))
aoc_lube.submit(year=2023, day=18, part=2, solution=lambda: polyarea(PART2))
