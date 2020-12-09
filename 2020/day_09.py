import aoc_helper
from itertools import combinations

raw = aoc_helper.day(9)

def parse_raw():
    return [int(line) for line in raw.splitlines()]

data = parse_raw()

def part_one():
    for i, n in enumerate(data[25:]):
        if n not in {x + y for x, y in combinations(data[i: i + 25], 2)}:
            return n

def part_two():
    target = 3199139634
    i = -1
    while i < len(data) - 2:
        i += 1       # start index
        j = i + 1    # end index
        n = data[i]  # n is our sum
        while n < target:
            n += data[j]
            if n > target:
                break
            elif n == target:
                r = data[i: j + 1]
                return max(r) + min(r)
            j += 1

print(part_two())
aoc_helper.submit(9, part_one)
aoc_helper.submit(9, part_two)
