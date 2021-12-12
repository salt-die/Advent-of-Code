import networkx as nx

import aoc_helper

RAW = aoc_helper.day(12)
CAVES = nx.Graph(line.split("-") for line in RAW.splitlines())

def npaths(current, revisited, seen=()):
    if current == "end":
        return 1

    if current.islower():
        if current not in seen:
            seen = {*seen, current}
        elif not revisited:
            revisited = True

    return sum(
        npaths(neighbor, revisited, seen)
        for neighbor in CAVES[current]
        if neighbor != "start"
        if neighbor not in seen or not revisited
    )

def part_one():
    return npaths("start", True)

def part_two():
    return npaths("start", False)

aoc_helper.submit(12, part_one)
aoc_helper.submit(12, part_two)
