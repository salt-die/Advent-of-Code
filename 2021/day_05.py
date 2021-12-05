import re

import cv2
import numpy as np

import aoc_helper

RAW = aoc_helper.day(5)

def parse_raw():
    for match in re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", RAW):
        a, b, c ,d = map(int, match)
        yield (a, b), (c, d)

DATA = tuple(parse_raw())

SHAPE = (
    max(max(a, b) for (_, a), (_, b) in DATA),
    max(max(a, b) for (a, _), (b, _) in DATA),
)

def intersects_from_lines(lines):
    image = np.zeros(SHAPE, dtype=int)

    for pt1, pt2 in lines:
        image += cv2.line(np.zeros_like(image), pt1, pt2, 1)

    return (image > 1).sum()

def is_not_diagonal(line):
    (x1, y1), (x2, y2) = line
    return x1 == x2 or y1 == y2

def part_one():
    return intersects_from_lines(filter(is_not_diagonal, DATA))

def part_two():
    return intersects_from_lines(DATA)

aoc_helper.submit(5, part_one)
aoc_helper.submit(5, part_two)
