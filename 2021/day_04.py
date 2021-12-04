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

def part_one():
    boards = BOARDS.copy()

    for number in NUMBERS:
        boards[boards == number] = -1

        for i in range(10):
            rows = np.all(boards[:, i//2] == -1, axis=1)

            if rows.any():
                board = boards[np.argwhere(rows)]
                board[board == -1] = 0
                return board.sum() * number

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
                board = boards[0]
                board[board == -1] = 0
                return board.sum() * number

            boards = np.swapaxes(boards, 1, 2)

aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)
