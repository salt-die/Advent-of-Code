from functools import cache
from itertools import starmap

import aoc_lube
from aoc_lube.utils import Vec2, sliding_window

CODES = aoc_lube.fetch(year=2024, day=21).splitlines()


NUMPAD = {
    key: Vec2(y, x)
    for y, row in enumerate(["789", "456", "123", "_0A", "<v>"])
    for x, key in enumerate(row)
}
NUMPAD["^"] = NUMPAD["0"]
OO = NUMPAD["_"]


def paths(a, b):
    u, v = NUMPAD[a], NUMPAD[b]
    Δ = v - u
    path = f"{'v' * Δ.y}{'^' * -Δ.y}{'>' * Δ.x}{'<' * -Δ.x}"
    if u.x != OO.x or v.y != OO.y:
        yield f"{path}A"
    if all(Δ) and (u.y != OO.y or v.x != OO.x):
        yield f"{path[::-1]}A"


@cache
def nkeys(code, nrobots=2):
    all_paths = starmap(paths, sliding_window("A" + code))
    if nrobots == 0:
        return sum(len(next(path)) for path in all_paths)
    return sum(min(nkeys(path, nrobots - 1) for path in paths) for paths in all_paths)


def part_one():
    return sum(nkeys(code) * int(code[:-1]) for code in CODES)


def part_two():
    return sum(nkeys(code, nrobots=25) * int(code[:-1]) for code in CODES)


aoc_lube.submit(year=2024, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=21, part=2, solution=part_two)
