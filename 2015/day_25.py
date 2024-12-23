import aoc_lube
from aoc_lube.utils import extract_ints

Y, X = extract_ints(aoc_lube.fetch(year=2015, day=25))
INITIAL = 20151125
EXP = 252533
MODULUS = 33554393


def nth(y, x):
    return (y + x - 1) * (y + x - 2) // 2 + x - 1


def part_one():
    return INITIAL * pow(EXP, nth(Y, X), MODULUS) % MODULUS


aoc_lube.submit(year=2015, day=25, part=1, solution=part_one)
