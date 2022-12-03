from itertools import chain

import aoc_lube
from aoc_lube.utils import chunk

RUCKSACKS = aoc_lube.fetch(year=2022, day=3).splitlines()

def priority(letter):
    offset = ord("a") if letter.islower() else (ord("A") - 26)
    return 1 + ord(letter) - offset

def part_one():
    return sum(map(priority,
        chain.from_iterable(
            set(rucksack[:(l := len(rucksack) // 2)]) & set(rucksack[l:])
            for rucksack in RUCKSACKS
        )
    ))

def part_two():
    return sum(map(priority,
        chain.from_iterable(
            set(a) & set(b) & set(c)
            for a, b, c in chunk(RUCKSACKS, 3)
        )
    ))

aoc_lube.submit(year=2022, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=3, part=2, solution=part_two)
