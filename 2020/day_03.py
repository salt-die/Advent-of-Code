import aoc_helper
import numpy as np
from utils import prod

raw = aoc_helper.day(3)

def parse_raw():
    # Turn input into a boolean array: True indicates a Tree
    return np.array([[char == "#" for char in line] for line in raw.splitlines()])

data = parse_raw()
h, w = data.shape

def trees_hit(x, y):
    """Return number of trees hit given a slope (x, y)."""
    xs = tuple((x * i) % w for i in range(1, h // y + bool(h % y)))
    ys = tuple(range(y, h, y))
    return data[ys, xs].sum()

def part_one():
    return trees_hit(3, 1)

def part_two():
    slopes = (1, 1), (3, 1), (5, 1), (7, 1), (1, 2)
    return prod(trees_hit(x, y) for x, y in slopes)

aoc_helper.submit(3, part_one)
aoc_helper.submit(3, part_two)
