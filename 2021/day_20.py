from scipy.ndimage import correlate
import numpy as np

import aoc_helper

def parse_raw():
    mapping, image = aoc_helper.day(20).split("\n\n")

    return (
        np.array([i == "#" for i in mapping]).astype(int),
        np.array([[i == "#" for i in line] for line in image.splitlines()]).astype(int),
    )

BIN_POWERS = 2**np.arange(9)[::-1].reshape(3, 3)
MAPPING, IMAGE = parse_raw()

def enhance(n):
    image = np.pad(IMAGE, n)

    for _ in range(n):
        image = MAPPING[correlate(image, BIN_POWERS)]

    return image

def part_one():
    return enhance(2).sum()

def part_two():
    return enhance(50).sum()

aoc_helper.submit(20, part_one)
aoc_helper.submit(20, part_two)
