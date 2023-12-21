from itertools import product

import aoc_lube
from aoc_lube.utils import GRID_NEIGHBORHOODS
from scipy.interpolate import lagrange

RAW = aoc_lube.fetch(year=2023, day=21)
GRID = RAW.splitlines()
H = len(GRID)
START = next((y, x) for (y, x) in product(range(H), repeat=2) if GRID[y][x] == "S")


def step(nodes):
    return {
        (y + dy, x + dx)
        for y, x in nodes
        for dy, dx in GRID_NEIGHBORHOODS[4]
        if GRID[(y + dy) % H][(x + dx) % H] != "#"
    }


def part_one():
    nodes = [START]
    for _ in range(64):
        nodes = step(nodes)
    return len(nodes)


def part_two():
    xs = [65, 65 + H, 65 + 2 * H]
    ys = []
    nodes = [START]
    for i in range(xs[-1]):
        nodes = step(nodes)
        if i + 1 in xs:
            ys.append(len(nodes))
    return round(lagrange(xs, ys)(26501365))


aoc_lube.submit(year=2023, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=21, part=2, solution=part_two)
