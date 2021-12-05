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

def intersections(lines):
    image = np.zeros((1000, 1000), dtype=int)

    for a, b in lines:
        image += cv2.line(np.zeros_like(image), a, b, 1)

    return (image > 1).sum()

def part_one():
    return intersections(
        ((a, b), (c, d))
        for ((a, b), (c, d)) in DATA
        if a == c or b == d
    )

def part_two():
    return intersections(DATA)

aoc_helper.submit(5, part_one)
aoc_helper.submit(5, part_two)
