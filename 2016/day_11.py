from collections import deque
from itertools import combinations, product
import re

import aoc_lube

def initial_config():
    item_re = re.compile(r"(\w+)(-compatible microchip| generator)")
    seen = {}
    names = iter("abcde")
    for line in aoc_lube.fetch(year=2016, day=11).splitlines():
        floor = set()
        for name, kind in item_re.findall(line):
            if name not in seen:
                seen[name] = next(names)
            floor.add(seen[name] + kind[1])
        yield frozenset(floor)

INITIAL_CONFIG = tuple(initial_config())

def is_valid_state(floors):
    return all(
        f"{a}g" in floor
        for floor in floors if any(b == "g" for _, b in floor)
        for a, b in floor if b == "c"
    )

def move_items(floors, elevator, dest, items):
    return tuple(
        floor ^ items if i == elevator else
        floor | items if i == dest else
        floor
        for i, floor in enumerate(floors)
    )

def hash_state(floors, elevator):
    n = elevator
    for i, floor in enumerate(floors, start=1):
        n += 16 ** (2 * i - 1) * len(floor)
        n += 16 ** (2 * i) * sum(b == "g" for _, b in floor)
    return n

def nmoves(initial_state):
    queue = deque([(initial_state, 0, 0)])
    seen = set()
    while queue:
        floors, elevator, nmoves = queue.popleft()

        if not any(floors[:3]):
            return nmoves

        if (hash_ := hash_state(floors, elevator)) in seen:
            continue

        seen.add(hash_)

        for nitems, direction in product((1, 2), (-1, 1)):
            for items in combinations(floors[elevator], nitems):
                if (dest := elevator + direction) < 0 or 4 <= dest:
                    continue

                new_floors = move_items(floors, elevator, dest, set(items))
                if is_valid_state(new_floors):
                    queue.append((new_floors, dest, nmoves + 1))

def part_one():
    return nmoves(INITIAL_CONFIG)

def part_two():
    a, *b = INITIAL_CONFIG
    return nmoves((a | {"yc", "yg", "zc", "zg"}, *b))

aoc_lube.submit(year=2016, day=11, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=11, part=2, solution=part_two)
