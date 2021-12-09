import re

import numpy as np
from scipy.ndimage import label

import aoc_helper

RAW = aoc_helper.day(9)

CAVE_MAP = np.fromiter(map(int, re.findall(r"\d", RAW)), dtype=int).reshape(100, 100)

def part_one():
    border_map = np.pad(CAVE_MAP, 1, mode="constant", constant_values=9)

    mask = (
          (CAVE_MAP < border_map[2:   , 1: -1])
        & (CAVE_MAP < border_map[ : -2, 1: -1])
        & (CAVE_MAP < border_map[1: -1, 2:   ])
        & (CAVE_MAP < border_map[1: -1,  : -2])
    )
    return (CAVE_MAP[mask] + 1).sum()

def part_two():
    labels, nlabels = label(CAVE_MAP != 9)
    labels = labels.reshape(-1)

    return np.partition(np.bincount(labels, labels != 0), nlabels - 3)[-3:].prod().astype(int)

aoc_helper.submit(9, part_one)
aoc_helper.submit(9, part_two)
