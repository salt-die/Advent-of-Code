import aoc_lube
from aoc_lube.utils import chunk, split

RUCKSACKS = aoc_lube.fetch(year=2022, day=3).splitlines()

def priority(s):
    letter = next(iter(s))
    offset = ord("a") if letter.islower() else (ord("A") - 26)
    return 1 + ord(letter) - offset

def part_one():
    return sum(
        priority(set(a) & set(b))
        for a, b in map(split, RUCKSACKS)
    )

def part_two():
    return sum(
        priority(set(a) & set(b) & set(c))
        for a, b, c in chunk(RUCKSACKS, 3)
    )

aoc_lube.submit(year=2022, day=3, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=3, part=2, solution=part_two)
