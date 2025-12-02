import aoc_lube
from aoc_lube.utils import chunk, extract_ints

DATA = list(chunk(extract_ints(aoc_lube.fetch(year=2025, day=2).replace("-", " ")), 2))


def is_valid(n: int):
    s = str(n)
    m = len(s) // 2
    return s[:m] != s[m:]


def invalids(a, b):
    s = str(a)
    if len(s) != len(str(b)):
        yield from invalids(a, int("9" * len(s)))
        yield from invalids(int("1" + "0" * len(s)), b)
        return

    seen = set()
    for i in range(1, len(s) // 2 + 1):
        if len(s) % i:
            continue
        initial = int(s[:i])
        while True:
            possible = int(str(initial) * (len(s) // i))
            if possible > b:
                break
            initial += 1
            if possible not in seen and possible >= a:
                seen.add(possible)
                yield possible


def part_one():
    total_invalid = 0
    for a, b in DATA:
        for n in range(a, b + 1):
            if not is_valid(n):
                total_invalid += n
    return total_invalid


def part_two():
    return sum(sum(invalids(a, b)) for a, b in DATA)


aoc_lube.submit(year=2025, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=2, part=2, solution=part_two)
