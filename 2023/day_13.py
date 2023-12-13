import aoc_lube
import numpy as np

DATA = [
    np.array([[*line] for line in pattern.splitlines()])
    for pattern in aoc_lube.fetch(year=2023, day=13).split("\n\n")
]


def reflect_axis(pattern, smudge):
    for i in range(1, len(pattern)):
        a = pattern[:i][::-1]
        b = pattern[i:]
        trim = min(len(a), len(b))
        if (a[:trim] != b[:trim]).sum() == smudge:
            return i
    return 0


def reflections(pattern, smudge):
    return 100 * reflect_axis(pattern, smudge) + reflect_axis(pattern.T, smudge)


def part_one():
    return sum(reflections(pattern, 0) for pattern in DATA)


def part_two():
    return sum(reflections(pattern, 1) for pattern in DATA)


aoc_lube.submit(year=2023, day=13, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=13, part=2, solution=part_two)
