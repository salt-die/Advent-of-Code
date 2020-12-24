import re

import aoc_helper
import numpy as np

def decode(tile):
    return tuple(sum((steps[direction] for direction in tile), start=np.array([0, 0])))

def init_config():
    DIRECTION_RE = re.compile(r"nw|ne|sw|se|w|e")
    tiles = (DIRECTION_RE.findall(line) for line in raw.splitlines())

    black = set()
    for tile in tiles:
        black.symmetric_difference_update((decode(tile), ))
    return black

def neighbors(tile, with_self=False):
    if with_self: yield tile
    yield from (tuple(np.array(tile) + neighbor) for neighbor in steps.values())

def update(n):
    seen = set()
    flip = set()
    for _ in range(n):
        for tile in black:
            for neighbor in neighbors(tile, with_self=True):
                if neighbor in seen:
                    continue
                seen.add(neighbor)

                s = sum(map(black.__contains__, neighbors(neighbor)))
                if neighbor in black and (s == 0 or s > 2) or neighbor not in black and s == 2:
                    flip.add(neighbor)

        black.symmetric_difference_update(flip)
        seen.clear()
        flip.clear()

def part_one():
    return len(black)

def part_two():
    update(100)
    return len(black)

raw = aoc_helper.day(24)

steps = {
    "e" : ( 0,  2),
    "w" : ( 0, -2),
    "se": ( 1,  1),
    "sw": ( 1, -1),
    "ne": (-1,  1),
    "nw": (-1, -1),
}

black = init_config()

aoc_helper.submit(24, part_one)
aoc_helper.submit(24, part_two)
