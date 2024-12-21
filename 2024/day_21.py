from functools import cache

import aoc_lube
from aoc_lube.utils import Vec2, sliding_window

CODES = aoc_lube.fetch(year=2024, day=21).splitlines()


def make_device(rows):
    return {key: Vec2(y, x) for y, row in enumerate(rows) for x, key in enumerate(row)}


ARROWS = make_device([["", "^", "A"], ["<", "v", ">"]])
NUMPAD = make_device(
    [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["", "0", "A"]]
)


def paths(a, b, keys):
    u, v, oob = keys[a], keys[b], keys[""]
    Δ = v - u
    moves = f"{'v' * Δ.y}{'^' * -Δ.y}{'>' * Δ.x}{'<' * -Δ.x}"
    if u.x != oob.x or v.y != oob.y:
        yield moves + "A"
    if Δ.x != 0 != Δ.y and (u.y != oob.y or v.x != oob.x):
        yield moves[::-1] + "A"


@cache
def min_keys(sequence, nrobots=2, robot=0):
    keys = ARROWS if robot else NUMPAD
    all_paths = (paths(a, b, keys) for a, b in sliding_window("A" + sequence))
    if robot == nrobots:
        return sum(len(next(path)) for path in all_paths)
    return sum(
        min(min_keys(path, nrobots, robot + 1) for path in paths) for paths in all_paths
    )


def part_one():
    return sum(min_keys(code) * int(code[:-1]) for code in CODES)


def part_two():
    return sum(min_keys(code, nrobots=25) * int(code[:-1]) for code in CODES)


aoc_lube.submit(year=2024, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=21, part=2, solution=part_two)
