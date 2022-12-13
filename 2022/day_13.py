from itertools import chain

import aoc_lube

PACKETS = [
    [eval(line) for line in block.splitlines()]
    for block in aoc_lube.fetch(year=2022, day=13).split("\n\n")
]

def cmp(a, b):
    match a, b:
        case int(), int():
            return a - b
        case int(), _:
            a = [a]
        case _, int():
            b = [b]

    for i, j in zip(a, b):
        if result := cmp(i, j):
            return result

    return len(a) - len(b)

def part_one():
    return sum(i for i, (a, b) in enumerate(PACKETS, start=1) if cmp(a, b) < 0)

def part_two():
    i, j = 1, 2
    for packet in chain.from_iterable(PACKETS):
        if cmp(packet, [[2]]) < 0:
            i += 1
            j += 1
        elif cmp(packet, [[6]]) < 0:
            j += 1

    return i * j

aoc_lube.submit(year=2022, day=13, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=13, part=2, solution=part_two)
