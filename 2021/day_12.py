import networkx as nx

import aoc_helper

RAW = aoc_helper.day(12)
CAVE = nx.Graph(line.split("-") for line in RAW.splitlines())

def npaths(current, seen=None, twice=None):
    if current == "end":
        return 1

    if seen is None:
        seen = set()

    if current.islower():
        if current not in seen:
            seen = seen.copy()
            seen.add(current)
        elif twice is True:
            twice = current

    return sum(
        npaths(neighbor, seen, twice)
        for neighbor in CAVE[current]
        if neighbor != "start"
        if neighbor not in seen or twice is True
    )

def part_one():
    return npaths("start")

def part_two():
    return npaths("start", twice=True)

aoc_helper.submit(12, part_one)
aoc_helper.submit(12, part_two)
