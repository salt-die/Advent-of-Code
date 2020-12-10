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

aoc_helper.submit(10, part_one)
aoc_helper.submit(10, part_two)
