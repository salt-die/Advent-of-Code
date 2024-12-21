from functools import cache

import aoc_lube
from aoc_lube.utils import Vec2, sliding_window

CODES = aoc_lube.fetch(year=2024, day=21).splitlines()


def make_keys(rows):
    return {key: Vec2(y, x) for y, row in enumerate(rows) for x, key in enumerate(row)}


ARROWS = make_keys(["h^A", "<v>"])
NUMPAD = make_keys(["789", "456", "123", "h0A"])


def paths(a, b, keys):
    u, v, hole = keys[a], keys[b], keys["h"]
    Δ = v - u
    ys = f"{'v' * Δ.y}{'^' * -Δ.y}"
    xs = f"{'>' * Δ.x}{'<' * -Δ.x}"
    if u.x != hole.x or v.y != hole.y:
        yield f"{ys}{xs}A"
    if Δ.x != 0 != Δ.y and (u.y != hole.y or v.x != hole.x):
        yield f"{xs}{ys}A"


@cache
def nkeys(code, nrobots=2, robot=0):
    keys = ARROWS if robot else NUMPAD
    all_paths = (paths(a, b, keys) for a, b in sliding_window("A" + code))
    if robot == nrobots:
        return sum(len(next(path)) for path in all_paths)
    return sum(
        min(nkeys(path, nrobots, robot + 1) for path in paths) for paths in all_paths
    )


def part_one():
    return sum(nkeys(code) * int(code[:-1]) for code in CODES)


def part_two():
    return sum(nkeys(code, nrobots=25) * int(code[:-1]) for code in CODES)


aoc_lube.submit(year=2024, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=21, part=2, solution=part_two)
