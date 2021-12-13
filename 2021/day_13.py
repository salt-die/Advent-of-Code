import re

import numpy as np

import aoc_helper

_points, _instructions = aoc_helper.day(13).split("\n\n")

PAPER = np.zeros((895, 1311), dtype=bool)
for x, y in re.findall(r"(\d+),(\d+)", _points):
    PAPER[int(y), int(x)] = 1

INSTRUCTIONS = [(axis, int(coord)) for axis, coord in re.findall(r"fold along ([xy])=(\d+)", _instructions)]

def fold(paper, axis, coord):
    match axis:
        case "x":
            return paper[:, :coord] | paper[:, -1: coord: -1]
        case "y":
            return paper[:coord] | paper[-1: coord: -1]

def part_one():
    return fold(PAPER, *INSTRUCTIONS[0]).sum()

def part_two():
    paper = PAPER
    for instruction in INSTRUCTIONS:
        paper = fold(paper, *instruction)

    aoc_helper.utils.dot_print(paper)

    return "JRZBLGKH"  # after inspection

aoc_helper.submit(13, part_one)
aoc_helper.submit(13, part_two)
