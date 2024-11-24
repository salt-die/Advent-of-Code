from collections import Counter, defaultdict

import aoc_lube
from aoc_lube.utils import extract_ints


def make_tally():
    log = [
        (*extract_ints(line[:18].replace("-", " ")), line[19:])
        for line in aoc_lube.fetch(year=2018, day=4).splitlines()
    ]
    log.sort()
    tally = defaultdict(Counter)
    for _, _, _, _, minute, event in log:
        if event.startswith("Guard"):
            guard = next(extract_ints(event))
        elif event == "falls asleep":
            start = minute
        else:
            for i in range(start, minute):
                tally[guard][i] += 1
    return tally


TALLY = make_tally()


def part_one():
    sleepiest = max(TALLY, key=lambda guard: sum(TALLY[guard].values()))
    return sleepiest * max(
        TALLY[sleepiest], key=lambda minute: TALLY[sleepiest][minute]
    )


def part_two():
    _, minute, guard = max(
        (n, minute, guard)
        for guard, counter in TALLY.items()
        for minute, n in counter.items()
    )
    return minute * guard


aoc_lube.submit(year=2018, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2018, day=4, part=2, solution=part_two)
