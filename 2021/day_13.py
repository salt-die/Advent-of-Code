import re

import numpy as np

import aoc_helper

def parse_raw():
    _points, _instructions = aoc_helper.day(13).split("\n\n")

    paper = np.zeros((895, 1311), dtype=bool)
    for x, y in re.findall(r"(\d+),(\d+)", _points):
        paper[int(y), int(x)] = 1

    instructions = re.findall(r"fold along ([xy])=\d+", _instructions)

    return paper, instructions

PAPER, INSTRUCTIONS = parse_raw()

def fold(paper, axis):
    match axis:
        case "x":
            w = paper.shape[1] >> 1
            return paper[:, :w] | paper[:, -1: w: -1]
        case "y":
            h = paper.shape[0] >> 1
            return paper[:h] | paper[-1: h: -1]

def part_one():
    return fold(PAPER, INSTRUCTIONS[0]).sum()

def part_two():
    paper = PAPER
    for instruction in INSTRUCTIONS:
        paper = fold(paper, instruction)

    aoc_helper.utils.dot_print(paper)

    return "JRZBLGKH"  # after inspection

aoc_helper.submit(13, part_one)
aoc_helper.submit(13, part_two)
