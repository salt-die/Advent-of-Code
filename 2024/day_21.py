from functools import cache
from itertools import starmap

import aoc_lube
from aoc_lube.utils import sliding_window

CODES = aoc_lube.fetch(year=2024, day=21).splitlines()
NUMPAD = {
    key: (y, x)
    for y, row in enumerate(["789", "456", "123", "_0A", "<v>"])
    for x, key in enumerate(row)
}
_Y, _X = NUMPAD["_"]


@cache
def paths(a, b):
    (uy, ux), (vy, vx) = NUMPAD[a], NUMPAD[b]
    dy, dx = vy - uy, vx - ux
    path = f"{'v' * dy}{'0' * -dy}{'>' * dx}{'<' * -dx}"
    paths = []
    if ux != _X or vy != _Y:
        paths.append(f"{path}A")
    if dy and dx and (uy != _Y or vx != _X):
        paths.append(f"{path[::-1]}A")
    return paths


@cache
def nkeys(code, nrobots=2):
    all_paths = starmap(paths, sliding_window("A" + code))
    if nrobots == 0:
        return sum(len(path[0]) for path in all_paths)
    return sum(min(nkeys(path, nrobots - 1) for path in paths) for paths in all_paths)


def part_one():
    return sum(nkeys(code) * int(code[:-1]) for code in CODES)


def part_two():
    return sum(nkeys(code, nrobots=25) * int(code[:-1]) for code in CODES)


aoc_lube.submit(year=2024, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=21, part=2, solution=part_two)
