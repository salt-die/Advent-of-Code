import aoc_helper

SANTAS_LIST = aoc_helper.day(8).splitlines()

def part_one():
    return sum(len(s) - len(eval(s)) for s in SANTAS_LIST)

def part_two():
    return sum(2 + s.count("\\") + s.count('"') for s in SANTAS_LIST)

aoc_helper.submit(8, part_one)
aoc_helper.submit(8, part_two)
