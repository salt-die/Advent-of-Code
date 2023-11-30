import aoc_lube
from aoc_lube.utils import sliding_window_cycle

RAW = aoc_lube.fetch(year=2017, day=1)


def part_one():
    return sum(int(a) if a == b else 0 for a, b in sliding_window_cycle(RAW))


def part_two():
    return sum(
        int(a) if a == b else 0
        for a, *_, b in sliding_window_cycle(RAW, len(RAW) // 2 - 1)
    )


aoc_lube.submit(year=2017, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2017, day=1, part=2, solution=part_two)
