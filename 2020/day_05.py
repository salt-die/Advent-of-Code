import aoc_helper

raw = aoc_helper.day(5)

def parse_raw():
    trans = str.maketrans('FBRL', '0110')

    for line in raw.splitlines():
        line = line.translate(trans)
        yield int(line[:-3], 2) * 8 + int(line[-3:], 2)

data = list(parse_raw())

def part_one():
    return max(data)

def part_two():
    l, m, s = len(data) + 1, min(data) - 1, sum(data)
    return (l * (l + 1) // 2 + l * m) - s

aoc_helper.submit(5, part_one)
aoc_helper.submit(5, part_two)
