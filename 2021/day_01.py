import aoc_helper

raw = aoc_helper.day(1)

data = list(aoc_helper.utils.extract_ints(raw))

def part_one():
    return sum(x < y for x, y in zip(data, data[1:]))

def part_two():
    return sum(x < y for x, y in zip(data, data[3:]))

aoc_helper.submit(1, part_one)
aoc_helper.submit(1, part_two)
