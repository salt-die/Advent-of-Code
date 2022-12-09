import aoc_lube
from aoc_lube.utils import int_grid

import numpy as np
import cv2

trees = int_grid(aoc_lube.fetch(year=2022, day=8)).astype(np.uint8)

def part_one():
    visible = np.zeros_like(trees, bool)
    visible[[0, -1]] = visible[:, [0, -1]] = True

    for i in range(4):
        dilated = np.maximum.accumulate(np.rot90(trees, i))
        dilated[1:] -= dilated[:-1]
        np.rot90(visible, i)[dilated.nonzero()] = True

    return visible.sum()

def part_two():
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    tall_trees = np.argwhere(cv2.dilate(trees, kernel, iterations=10) == trees) # Local maxima

    score = 0
    for y, x in tall_trees:
        prod = 1
        for s in (
            np.s_[y, x - 100::-1],
            np.s_[y, x + 1:],
            np.s_[y - 100::-1, x],
            np.s_[y + 1:, x],
        ):
            line = trees[y, x] > trees[s]
            prod *= len(line) if line.all() else line.argmin() + 1
        score = max(score, prod)

    return score

aoc_lube.submit(year=2022, day=8, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=8, part=2, solution=part_two)
