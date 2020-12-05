import aoc_helper

raw = aoc_helper.day(5)

trans = str.maketrans('FBRL', '0110')
data = [int(line.translate(trans), 2) for line in raw.splitlines()]

def part_one():
    return max(data)

def part_two():
    l, m = len(data) + 1, min(data) - 1,
    return l * (l + 1) // 2 + l * m - sum(data)

aoc_helper.submit(5, part_one)
aoc_helper.submit(5, part_two)
