import numpy as np

import aoc_helper
from aoc_helper.utils import extract_ints

RAW = aoc_helper.day(4)

def parse_raw():
    numbers, *boards = RAW.split("\n\n")

    return (
        tuple(extract_ints(numbers)),
        np.array(
            [np.fromiter(extract_ints(board), dtype=int) for board in boards]
        ).reshape(-1, 5, 5),
    )

NUMBERS, BOARDS = parse_raw()

def score(board, number):
    return np.where(board == -1, 0, board).sum() * number

def part_one():
    boards = BOARDS.copy()

    for number in NUMBERS:
        boards[boards == number] = -1

        for i in range(10):
            rows = np.all(boards[:, i//2] == -1, axis=1)
            if rows.any():
                return score(boards[np.argwhere(rows)], number)

            boards = np.swapaxes(boards, 1, 2)

def part_two():
    boards = BOARDS.copy()

    for number in NUMBERS:
        boards[boards == number] = -1

        for i in range(10):
            rows = np.all(boards[:, i//2] == -1, axis=1)

            if len(boards) > 1:
                boards = boards[~rows]
            elif rows[0]:
                return score(boards[0], number)

            boards = np.swapaxes(boards, 1, 2)

aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)
