import aoc_lube
from aoc_lube.utils import dot_print

import numpy as np
from parse import parse

def produce_screen():
    screen = np.zeros((6, 50), bool)
    for instruction in aoc_lube.fetch(year=2016, day=8).splitlines():
        if match := parse("rect {:d}x{:d}", instruction):
            x, y = match
            screen[:y, :x] = ~screen[:y, :x]
        elif match := parse("rotate column x={:d} by {:d}", instruction):
            col, shift = match
            screen[:, col] = np.roll(screen[:, col], shift)
        elif match := parse("rotate row y={:d} by {:d}", instruction):
            row, shift = match
            screen[row] = np.roll(screen[row], shift)
    return screen

SCREEN = produce_screen()

def part_one():
    return SCREEN.sum()

def part_two():
    dot_print(SCREEN)
    return "EFEYKFRFIJ"

aoc_lube.submit(year=2016, day=8, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=8, part=2, solution=part_two)
