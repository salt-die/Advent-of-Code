import re

import numpy as np

import aoc_helper

LIGHTS = np.zeros((1000, 1000), dtype=int)
DATA = [
    (command, LIGHTS[int(y1): int(y2) + 1, int(x1): int(x2) + 1])
    for command, y1, x1, y2, x2 in re.findall(
        r"(?:turn )*(.*) (\d+),(\d+) through (\d+),(\d+)\n*",
        aoc_helper.day(6),
    )
]

def do_lights(off, on, toggle):
    LIGHTS[:] = 0
    for command, view in DATA:
        exec(locals()[command])
    return LIGHTS.sum()

def part_one():
    return do_lights("view[:] = 0", "view[:] = 1", "view ^= 1")

def part_two():
    return do_lights("view[view > 0] -= 1", "view += 1", "view += 2")

aoc_helper.submit(6, part_one)
aoc_helper.submit(6, part_two)
