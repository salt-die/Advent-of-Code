from collections import Counter
from itertools import combinations

import aoc_lube
from aoc_lube.utils import chunk, extract_ints

DATA = list(chunk(extract_ints(aoc_lube.fetch(year=2025, day=2).replace("-", " ")), 2))


def is_valid(n: int):
    s = str(n)
    m = len(s) // 2
    return s[:m] != s[m:]


def part_one():
    total_invalid = 0
    for a, b in DATA:
        for n in range(a, b + 1):
            if not is_valid(n):
                total_invalid += n
    return total_invalid


def fold_div(it) -> int:
    all_div = it[0]
    for a in it[1:]:
        if all_div % a:
            all_div = 1
        else:
            all_div = a
    return all_div


def sum_of_invalids(a: int, b: int) -> int:
    s = str(a)
    if len(s) != len(str(b)):
        m = int("9" * len(s))
        return sum_of_invalids(a, m) + sum_of_invalids(m + 1, b)

    seen = Counter()
    for i in range(len(s) // 2, 0, -1):
        if len(s) % i:
            continue

        initial = int(s[:i])
        while True:
            possible = int(str(initial) * (len(s) // i))
            if possible > b:
                break
            if possible >= a:
                seen[i] += possible
            initial += 1

    total = 0
    for i in range(1, len(seen) + 1):
        for d in combinations(seen, r=i):
            total += seen[fold_div(d)] * (-1) ** (i + 1)
    return total


def part_two():
    return sum(sum_of_invalids(a, b) for a, b in DATA)


aoc_lube.submit(year=2025, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=2, part=2, solution=part_two)
