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
    i = -1
    while i < len(data) - 2:
        i += 1       # start index
        j = i + 1    # end index
        n = mn = mx = data[i]  # n is our sum, mn is minimun, mx is max
        while n < target:
            if data[j] < mn:
                mn = data[j]
            elif data[j] > mx:
                mx = data[j]

            n += data[j]
            if n > target:
                break
            elif n == target:
                return mx + mn
            j += 1
print(part_one())
aoc_helper.submit(9, part_one)
aoc_helper.submit(9, part_two)
