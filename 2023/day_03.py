import re
from math import prod

import aoc_lube

GRID = aoc_lube.fetch(year=2023, day=3).splitlines()
MATCHES = [list(re.finditer(r"(\d+)", line)) for line in GRID]
SYMBOLS = {}


def find_symbol(y, match):
    for v in [y - 1, y, y + 1]:
        for u in range(match.start() - 1, match.end() + 1):
            if (
                0 <= v < len(GRID)
                and 0 <= u < len(GRID[0])
                and GRID[v][u] != "."
                and not GRID[v][u].isdigit()
            ):
                return v, u


def find_all_symbols():
    for y, line in enumerate(MATCHES):
        for match in line:
            if symbol := find_symbol(y, match):
                SYMBOLS.setdefault(symbol, []).append(int(match[1]))


find_all_symbols()


def part_one():
    return sum(sum(parts) for parts in SYMBOLS.values())


def part_two():
    return sum(
        prod(parts)
        for (y, x), parts in SYMBOLS.items()
        if GRID[y][x] == "*" and len(parts) == 2
    )


aoc_lube.submit(year=2023, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=3, part=2, solution=part_two)
