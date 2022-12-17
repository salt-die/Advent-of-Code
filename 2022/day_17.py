from itertools import cycle

import aoc_lube
import numpy as np

DIRECTIONS = cycle(enumerate(1 if c == ">" else -1 for c in aoc_lube.fetch(year=2022, day=17)))
PIECES = cycle(enumerate(
    np.array(piece, bool)
    for piece in (
        [[1, 1, 1, 1]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
        [[1], [1], [1], [1]],
        [[1, 1], [1, 1]],
)))

def collides(y, x, piece, matrix):
    h, w = piece.shape
    return x < 0 or 7 < x + w or y < 0 or (matrix[y: y + h, x: x + w] & piece).any()

def tetrish(npieces, matrix_height=5_000):
    matrix = np.zeros((matrix_height, 7), bool)
    height = 0
    cycle_detection = {}

    for n, (i, piece) in enumerate(PIECES):
        if n == npieces:
            return height

        y, x = 3 + height, 2
        for j, dx in DIRECTIONS:
            if not collides(y, x + dx, piece, matrix):
                x += dx
            if not collides(y - 1, x, piece, matrix):
                y -= 1
            else:
                break

        if (i, j) in cycle_detection:
            prev_n, prev_height = cycle_detection[i, j]
            d, r = divmod(npieces - n, n - prev_n)
            if r == 0:
                return d * (height - prev_height) + height
        else:
            cycle_detection[i, j] = n, height

        h, w = piece.shape
        matrix[y: y + h, x: x + w][piece] = 1
        height = max(height, y + h)

def part_one():
    return tetrish(2022)

def part_two():
    return tetrish(1_000_000_000_000)

aoc_lube.submit(year=2022, day=17, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=17, part=2, solution=part_two)
