import re
from collections import Counter
from math import prod

import aoc_lube


def parse_raw():
    for line in aoc_lube.fetch(year=2023, day=2).splitlines():
        cubes = Counter()
        for n, color in re.findall(r"(\d+) (\w+)", line):
            if int(n) > cubes[color]:
                cubes[color] = int(n)
        yield int(re.search(r"Game (\d+)", line)[1]), cubes


GAMES = list(parse_raw())


def part_one():
    max_cubes = Counter({"red": 12, "green": 13, "blue": 14})
    return sum(id for id, game in GAMES if game <= max_cubes)


def part_two():
    return sum(prod(game.values()) for _, game in GAMES)


aoc_lube.submit(year=2023, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=2, part=2, solution=part_two)
