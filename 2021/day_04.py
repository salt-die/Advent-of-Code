from io import StringIO

import numpy as np

import aoc_helper

RAW = aoc_helper.day(4)

def parse_raw():
    numbers, boards = RAW.split("\n\n", 1)

    return (
        tuple(aoc_helper.utils.extract_ints(numbers)),
        np.loadtxt(StringIO(boards), dtype=int).reshape(-1, 5, 5),
    )

NUMBERS, BOARDS = parse_raw()

def part_one():
    boards = BOARDS.copy()

    for number in NUMBERS:
        boards[boards == number] = -1

        mask = boards == -1
        winners = (mask.all(1) | mask.all(2)).any(1)

        if winners.any():
            boards[boards == -1] = 0
            return boards[winners].sum() * number

def part_two():
    boards = BOARDS.copy()

    for number in NUMBERS:
        boards[boards == number] = -1

        mask = boards == -1
        winners = (mask.all(1) | mask.all(2)).any(1)

        if len(boards) > 1:
            boards = boards[~winners]
        elif winners[0]:
            boards[boards == -1] = 0
            return boards.sum() * number

aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)
