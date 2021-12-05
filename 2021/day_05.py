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

def init_image():
    max_x = max(max(a, b) for (a, _), (b, _) in DATA)
    max_y = max(max(a, b) for (_, a), (_, b) in DATA)

    return np.zeros((max_y, max_x), dtype=int)

def add_line(image, pt1, pt2, no_diagonal=True):
    x1, y1 = pt1
    x2, y2 = pt2

    if not no_diagonal or x1 == x2 or y1 == y2:
        image += cv2.line(np.zeros_like(image), pt1, pt2, 1)

def part_one():
    image = init_image()

    for pt1, pt2 in DATA:
        add_line(image, pt1, pt2, no_diagonal=True)

    return (image > 1).sum()

def part_two():
    image = init_image()

    for pt1, pt2 in DATA:
        add_line(image, pt1, pt2, no_diagonal=False)

    return (image > 1).sum()

aoc_helper.submit(5, part_one)
aoc_helper.submit(5, part_two)
