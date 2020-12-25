import re
import aoc_helper

raw = aoc_helper.day(24)
STEPS = {
    "e" :  0 + 2j,
    "w" :  0 - 2j,
    "se":  1 + 1j,
    "sw":  1 - 1j,
    "ne": -1 + 1j,
    "nw": -1 - 1j,
}

def decode(tile):
    return sum(STEPS[direction] for direction in tile)

def init_config():
    DIRECTION_RE = re.compile(r"nw|ne|sw|se|w|e")
    tiles = map(DIRECTION_RE.findall, raw.splitlines())

    black = set()
    for tile in tiles:
        black.symmetric_difference_update({decode(tile)})
    return black

def neighbors(tile, with_self=False):
    if with_self: yield tile
    yield from (tile + neighbor for neighbor in STEPS.values())

def update(n):
    seen = set()
    flipped = set()
    for _ in range(n):
        for tile in black:
            for neighbor in neighbors(tile, with_self=True):
                if neighbor in seen:
                    continue
                seen.add(neighbor)

                s = sum(neighbors_neighbor in black for neighbors_neighbor in neighbors(neighbor))
                if neighbor in black and (s == 0 or s > 2) or neighbor not in black and s == 2:
                    flipped.add(neighbor)

        black.symmetric_difference_update(flipped)
        seen.clear()
        flipped.clear()

def part_one():
    return len(black)

def part_two():
    update(100)
    return len(black)

black = init_config()

aoc_helper.submit(24, part_one)
aoc_helper.submit(24, part_two)
