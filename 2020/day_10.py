from functools import lru_cache

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
    return (diffs == 3).sum() * (diffs == 1).sum()

@lru_cache
def count_from_(i):
    if i == len(data) - 1:
        return 1
    return sum(count_from_(i + k) for k in range(1, min(4, len(data) - i)) if data[k + i] - data[i] <= 3)

def part_two():
    return count_from_(0)

aoc_helper.submit(10, part_one)
aoc_helper.submit(10, part_two)
