import aoc_lube
from aoc_lube.utils import dot_print

import numpy as np

def init_cycles():
    register = 1
    for line in aoc_lube.fetch(year=2022, day=10).splitlines():
        yield register
        if line[0] != "n":
            yield register
            register += int(line[5:])

def part_one():
    cycles = list(init_cycles())
    return sum(i * cycles[i - 1] for i in range(20, 221, 40))

def part_two():
    screen = np.zeros((6, 40), bool)
    for i, register in enumerate(init_cycles()):
        y, x = divmod(i, 40)
        screen[y, x] = abs(register - x) < 2

    dot_print(screen)

aoc_lube.submit(year=2022, day=10, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=10, part=2, solution=lambda: "EPJBRKAH")
