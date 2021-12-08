import re

import aoc_helper

RAW = aoc_helper.day(8)
DIGIT_RE = re.compile(r"[a-g]+")
DATA = [DIGIT_RE.findall(line) for line in RAW.splitlines()]
DECODE = {
    (6, 2, 3): "0",
    (2, 2, 2): "1",
    (5, 1, 2): "2",
    (5, 2, 3): "3",
    (4, 2, 4): "4",
    (5, 1, 3): "5",
    (6, 1, 3): "6",
    (3, 2, 2): "7",
    (7, 2, 4): "8",
    (6, 2, 4): "9",
}

def decode():
    for patterns in DATA:
        one, _, four, *_ = sorted(patterns[:-4], key=len)
        one = set(one)
        four = set(four)

        yield "".join(
            DECODE[
                len(digit),
                len(one.intersection(digit)),
                len(four.intersection(digit)),
            ]
            for digit in patterns[-4:]
        )

def part_one():
    return sum(
        digit in {"1", "4", "7", "8"}
        for output in decode()
        for digit in output
    )

def part_two():
    return sum(map(int, decode()))

aoc_helper.submit(8, part_one)
aoc_helper.submit(8, part_two)
