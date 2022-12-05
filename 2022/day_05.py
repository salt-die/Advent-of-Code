import aoc_lube
from aoc_lube.utils import extract_ints, chunk

def parse_raw():
    stacks, commands = aoc_lube.fetch(year=2022, day=5).split("\n\n")

    stacks = stacks.splitlines()
    stacks = [
        [stacks[y][x] for y in range(7, -1, -1) if stacks[y][x] != " "]
        for x in range(1, 35, 4)
    ]

    return stacks, tuple(chunk(extract_ints(commands), 3))

STACKS, COMMANDS = parse_raw()

def part_one():
    for a, b, c in COMMANDS:
        for _ in range(a):
            STACKS[c - 1].append(STACKS[b - 1].pop())

    return "".join(map(list.pop, STACKS))

def part_two():
    for a, b, c in COMMANDS:
        STACKS[c - 1].extend(STACKS[b - 1][-a:])
        del STACKS[b - 1][-a:]

    return "".join(map(list.pop, STACKS))

aoc_lube.submit(year=2022, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=5, part=2, solution=part_two)
