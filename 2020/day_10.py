from collections import deque

import aoc_helper
import numpy as np

raw = aoc_helper.day(10)

def parse_raw():
    jolts = list(aoc_helper.extract_ints(raw))
    jolts += 0, max(jolts) + 3
    return sorted(jolts)

data = parse_raw()

def part_one():
    diffs = np.diff(data)
    return (diffs == 1).sum() * (diffs == 3).sum()

def part_two():
    it = reversed(data)
    counts = deque(((next(it), 1), ), maxlen=3)

    for i in it:
        counts.append((i, s := sum(k for j, k in counts if j - i <= 3)))

    return s

aoc_helper.submit(10, part_one)
aoc_helper.submit(10, part_two)
