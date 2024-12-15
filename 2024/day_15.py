import aoc_lube
import numpy as np
from aoc_lube.utils import Vec2


def parse_raw():
    map_, instructions = aoc_lube.fetch(year=2024, day=15).split("\n\n")
    grid = map_.splitlines()
    h, w = len(grid), len(grid[0])
    warehouse_1 = np.full((h, w), "#")
    warehouse_2 = np.full((h, 2 * w), "#")
    for y, line in enumerate(map_.splitlines()):
        for x, char in enumerate(line):
            if char == "@" or char == ".":
                if char == "@":
                    start = Vec2(y, x)
                chars = "..."
            elif char == "O":
                chars = "O[]"
            else:
                chars = "###"
            warehouse_1[y, x], warehouse_2[y, 2 * x], warehouse_2[y, 2 * x + 1] = chars

    dirs = {"<": Vec2(0, -1), "^": Vec2(-1, 0), "v": Vec2(1, 0), ">": Vec2(0, 1)}

    return (
        start,
        warehouse_1,
        warehouse_2,
        [dirs[instruction] for instruction in instructions.replace("\n", "")],
    )


START, WAREHOUSE_1, WAREHOUSE_2, DIRECTIONS = parse_raw()


def part_one():
    current_pos = START
    for direction in DIRECTIONS:
        new_pos = current_pos + direction
        if WAREHOUSE_1[new_pos] == ".":
            current_pos = new_pos
        elif WAREHOUSE_1[new_pos] == "#":
            continue

        look_ahead = new_pos
        while WAREHOUSE_1[look_ahead] == "O":
            look_ahead += direction
        if WAREHOUSE_1[look_ahead] == "#":
            continue
        WAREHOUSE_1[look_ahead] = "O"
        WAREHOUSE_1[new_pos] = "."
        current_pos = new_pos

    return (np.argwhere(WAREHOUSE_1 == "O") * (100, 1)).sum()


def can_vertical_push(pos, dir):
    adj_pos = Vec2(0, 1) if WAREHOUSE_2[pos] == "[" else Vec2(0, -1)
    new_pos = pos + dir
    if WAREHOUSE_2[new_pos] == "#" or WAREHOUSE_2[new_pos + adj_pos] == "#":
        return False

    if WAREHOUSE_2[new_pos] in "[]" and not can_vertical_push(new_pos, dir):
        return False

    if WAREHOUSE_2[new_pos + adj_pos] in "[]" and not can_vertical_push(
        new_pos + adj_pos, dir
    ):
        return False
    return True


def do_vertical_push(pos, dir):
    adj_pos = Vec2(0, 1) if WAREHOUSE_2[pos] == "[" else Vec2(0, -1)
    new_pos = pos + dir
    if WAREHOUSE_2[new_pos] in "[]":
        do_vertical_push(new_pos, dir)

    if WAREHOUSE_2[new_pos + adj_pos] in "[]":
        do_vertical_push(new_pos + adj_pos, dir)

    WAREHOUSE_2[new_pos] = WAREHOUSE_2[pos]
    WAREHOUSE_2[new_pos + adj_pos] = WAREHOUSE_2[pos + adj_pos]
    WAREHOUSE_2[pos] = WAREHOUSE_2[pos + adj_pos] = "."


def part_two():
    current_pos = Vec2(START.y, 2 * START.x)
    for direction in DIRECTIONS:
        new_pos = current_pos + direction
        if WAREHOUSE_2[new_pos] == ".":
            current_pos = new_pos
        elif WAREHOUSE_2[new_pos] == "#":
            pass
        elif direction.x:
            look_ahead = new_pos
            while WAREHOUSE_2[look_ahead] in "[]":
                look_ahead += direction
            if WAREHOUSE_2[look_ahead] == "#":
                continue
            while look_ahead != new_pos:
                WAREHOUSE_2[look_ahead] = WAREHOUSE_2[look_ahead - direction]
                look_ahead -= direction
            WAREHOUSE_2[new_pos] = "."
            current_pos = new_pos
        elif can_vertical_push(new_pos, direction):
            do_vertical_push(new_pos, direction)
            current_pos = new_pos
    return (np.argwhere(WAREHOUSE_2 == "[") * (100, 1)).sum()


aoc_lube.submit(year=2024, day=15, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=15, part=2, solution=part_two)
