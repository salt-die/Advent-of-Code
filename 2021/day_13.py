import re

import numpy as np

import aoc_helper

POINT_RE = re.compile(r"(\d+),(\d+)")
INSTRUCTION_RE = re.compile(r"fold along ([xy])=(\d+)")

_points, _instructions = aoc_helper.day(13).split("\n\n")

PAPER = np.zeros((895, 1311), dtype=bool)
for x, y in POINT_RE.findall(_points):
    PAPER[int(y), int(x)] = 1

instructions = [
    (axis, int(coord))
    for axis, coord in INSTRUCTION_RE.findall(_instructions)
]

def fold(paper, axis, coord):
    match axis:
        case "x":
            return paper[:, :coord] | paper[:, -1: coord: -1]
        case "y":
            return paper[:coord] | paper[-1: coord: -1]

def part_one():
    return fold(PAPER, *instructions[0]).sum()

def part_two():
    paper = PAPER
    for axis, coord in instructions:
        paper = fold(paper, axis, coord)

    aoc_helper.utils.dot_print(paper)

    return "JRZBLGKH"  # After inspection

aoc_helper.submit(13, part_one)
aoc_helper.submit(13, part_two)
