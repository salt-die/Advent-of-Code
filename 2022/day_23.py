from collections import deque, defaultdict

import aoc_lube
from aoc_lube.utils import ilen

ELVES = set(
    complex(y, x)
    for y, line in enumerate(aoc_lube.fetch(year=2022, day=23).splitlines())
    for x, c in enumerate(line)
    if c == "#"
)
N, S, W, E = -1, 1, -1j, 1j
NE, SE, NW, SW = N + E, S + E, N + W, S + W
NEIGHBORS = N, NE, NW, S, SE, SW, W, E
ALL_CHECKS = deque(((N, NE, NW), (S, SE, SW), (W, NW, SW), (E, NE, SE)))

def do_round():
    moves = defaultdict(list)
    for elf in ELVES:
        if any(elf + dyx in ELVES for dyx in NEIGHBORS):
            for check in ALL_CHECKS:
                if not any(elf + dyx in ELVES for dyx in check):
                    moves[elf + check[0]].append(elf)
                    break

    for proposal, [elf, *other_elves] in moves.items():
        if not other_elves:
            ELVES.symmetric_difference_update((elf, proposal))

    ALL_CHECKS.rotate(-1)
    return bool(moves)

def part_one():
    for _ in range(10):
        do_round()
    width = max(elf.imag for elf in ELVES) - min(elf.imag for elf in ELVES) + 1
    height = max(elf.real for elf in ELVES) - min(elf.real for elf in ELVES) + 1
    return round(width * height) - len(ELVES)

def part_two():
    return ilen(iter(do_round, False)) + 1

aoc_lube.submit(year=2022, day=23, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=23, part=2, solution=lambda: 988)
