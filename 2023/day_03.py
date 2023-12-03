import re

import aoc_lube

GRID = aoc_lube.fetch(year=2023, day=3).splitlines()
H, W = len(GRID), len(GRID[0])
MATCHES = [
    [(int(m[1]), m.span()) for m in re.finditer(r"(\d+)", line)] for line in GRID
]
COORDS = {}


def find_symbol(y, x1, x2):
    for v in [y - 1, y, y + 1]:
        for u in range(x1 - 1, x2 + 1):
            if 0 <= v < H and 0 <= u < W and GRID[v][u] not in ".0123456789":
                return v, u


def find_all_symbols():
    for y, line in enumerate(MATCHES):
        for part, (x1, x2) in line:
            if coord := find_symbol(y, x1, x2):
                COORDS.setdefault(coord, []).append(part)


find_all_symbols()


def part_one():
    return sum(sum(parts) for parts in COORDS.values())


def part_two():
    return sum(a * b[0] for a, *b in COORDS.values() if b)


aoc_lube.submit(year=2023, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=3, part=2, solution=part_two)

# Alternative solution: Use rectangular regions to determine parts
# ----------------------------------------------------------------
# from rects import Rect, Region

# operators = Region()
# for y, line in enumerate(GRID):
#     for m in re.finditer(r"([^\d\.])", line):
#         operators |= Region.from_rect(Rect(m.start(), y, 1, 1))

# print(
#     sum(
#         int(m[1])
#         for y, line in enumerate(GRID)
#         for m in re.finditer(r"(\d+)", line)
#         if Region.from_rect(Rect(m.start() - 1, y - 1, len(m[1]) + 2, 3)) & operators
#     )
# )

# Alternative solution: Use a convolution
# ---------------------------------------
# import numpy as np
# from scipy.ndimage import convolve

# operators = np.array(
#     [[int(char != "." and not char.isdigit()) for char in line] for line in GRID]
# )
# spread = convolve(operators, np.ones((3, 3))).astype(bool)
# coded = np.zeros((H, W), int)
# numbers = []
# for y, line in enumerate(GRID):
#     for m in re.finditer(r"(\d+)", line):
#         numbers.append(int(m[0]))
#         coded[y, m.start() : m.end()] = len(numbers)
# translate = np.array(numbers)
# print(translate[np.unique(coded[spread & (coded != 0)] - 1)].sum())
