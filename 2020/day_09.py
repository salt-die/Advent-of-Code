import aoc_helper
from itertools import combinations

raw = aoc_helper.day(9)

def parse_raw():
    return [int(line) for line in raw.splitlines()]

data = parse_raw()

def part_one():
    for i, n in enumerate(data[25:]):
        s = set(data[i: i + 25])
        if not any(n - x in s for x in s):
            return n

def part_two():
    target = 3199139634
    i, j, n = 0, 1, sum(data[:2])
    while n != target:
        if n < target:
            j += 1
            n += data[j]
        else:
            n -= data[i]
            i += 1
    return max(s := data[i: j + 1]) + min(s)

print(part_two())
aoc_helper.submit(9, part_one)
aoc_helper.submit(9, part_two)
