from itertools import groupby
from math import prod

import aoc_helper
from more_itertools import ilen
import numpy as np

raw = aoc_helper.day(10)

def parse_raw():
    jolts = list(aoc_helper.extract_ints(raw))
    jolts += 0, max(jolts) + 3
    return sorted(jolts)

data = parse_raw()
diffs = np.diff(data)

def part_one():
    return (diffs == 1).sum() * (diffs == 3).sum()

def part_two():
    return prod((n := ilen(s)) * (n - 1) // 2 + 1 for g, s in groupby(diffs) if g == 1)

# Alternative solution with a deque of length 3:
# def part_two():
#     it = iter(data)
#     counts = deque([(next(it), 1)], maxlen=3)

#     for i in it:
#         counts.append((i, s := sum(k for j, k in counts if i - j <= 3)))

#     return s

aoc_helper.submit(10, part_one)
aoc_helper.submit(10, part_two)
