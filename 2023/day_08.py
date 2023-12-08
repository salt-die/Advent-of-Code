import re
from itertools import cycle
from math import lcm

import aoc_lube
from aoc_lube.utils import chunk


def parse_raw():
    instructions, network = aoc_lube.fetch(year=2023, day=8).split("\n\n")
    yield [int(instruction == "R") for instruction in instructions]
    yield {a: b for a, *b in chunk(re.findall(r"\w+", network), 3)}


INSTRUCTIONS, NETWORK = parse_raw()


def traverse(start, end_condition):
    current = start
    for i, dir in enumerate(cycle(INSTRUCTIONS)):
        current = NETWORK[current][dir]
        if end_condition(current):
            return i + 1


def part_one():
    return traverse("AAA", lambda node: node == "ZZZ")


def part_two():
    dist = (
        traverse(node, lambda node: node.endswith("Z"))
        for node in NETWORK
        if node.endswith("A")
    )
    return lcm(*dist)


aoc_lube.submit(year=2023, day=8, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=8, part=2, solution=part_two)
