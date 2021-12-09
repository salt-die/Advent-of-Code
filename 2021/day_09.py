import re
from heapq import nlargest
from math import prod

import cv2
import numpy as np
from scipy.ndimage import label

import aoc_helper

RAW = aoc_helper.day(9)

CAVE_MAP = np.fromiter(map(int, re.findall(r"\d", RAW)), dtype=int).reshape(100, 100)
BORDER_MAP = cv2.copyMakeBorder(CAVE_MAP, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=9)

def part_one():
    mask = (
          (CAVE_MAP < BORDER_MAP[2:   , 1: -1])
        & (CAVE_MAP < BORDER_MAP[ : -2, 1: -1])
        & (CAVE_MAP < BORDER_MAP[1: -1, 2:   ])
        & (CAVE_MAP < BORDER_MAP[1: -1,  : -2])
    )
    return (CAVE_MAP[mask] + 1).sum()

def part_two():
    labels, nbins = label(CAVE_MAP != 9)

    bin_sizes = ((labels == i).sum() for i in range(1, nbins + 1))

    return prod(nlargest(3, bin_sizes))

aoc_helper.submit(9, part_one)
aoc_helper.submit(9, part_two)
