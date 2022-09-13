import numpy as np
from cv2 import filter2D, BORDER_CONSTANT

import aoc_helper

GRID = np.array([list(line) for line in aoc_helper.day(18).splitlines()]) == "#"
KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

def step_grid(corners):
    grid = GRID.copy()
    for _ in range(100):
        neighbors = filter2D(grid.astype(np.uint8), -1, KERNEL, borderType=BORDER_CONSTANT)
        grid = (grid & (neighbors > 1) & (neighbors < 4)) | (~grid & (neighbors == 3))
        if corners:
            grid[(0, -1, 0, -1), (0, 0, -1, -1)] = 1

    return grid.sum()

def part_one():
    return step_grid(corners=False)

def part_two():
    return step_grid(corners=True)

aoc_helper.submit(18, part_one)
aoc_helper.submit(18, part_two)
