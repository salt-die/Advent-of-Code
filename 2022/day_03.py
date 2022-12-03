from functools import reduce

import aoc_lube
from aoc_lube.utils import chunk, split

RUCKSACKS = aoc_lube.fetch(year=2022, day=3).splitlines()

def priority(letter):
    offset = ord("a") if letter.islower() else (ord("A") - 26)
    return 1 + ord(letter) - offset

def sum_priorities(iterable):
    return sum(
        priority(*reduce(set.intersection, map(set, sacks)))
        for sacks in iterable
    )

def part_one():
    return sum_priorities(map(split, RUCKSACKS))

def part_two():
    return sum_priorities(chunk(RUCKSACKS, 3))

aoc_lube.submit(year=2022, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=3, part=2, solution=part_two)
