import numpy as np

import aoc_helper
from aoc_helper.utils import extract_ints

RAW = aoc_helper.day(4)

def parse_raw():
    draws, boards = RAW.split("\n\n", 1)

    return (
        np.fromiter(extract_ints(draws), dtype=int),
        np.fromiter(extract_ints(boards), dtype=int).reshape(-1, 5, 5),
    )

DRAWS, BOARDS = parse_raw()

def score_ith_winner(i):
    """
    Return the score of the ith winner.
    """
    draw_indices = DRAWS.argsort()[BOARDS]

    win_turns = np.minimum(
        draw_indices.max(1).min(1),  # min win turn for columns
        draw_indices.max(2).min(1),  # min win turn for rows
    )

    ith_win_index = win_turns.argsort()[i]

    ith_win_turn = win_turns[ith_win_index]
    ith_win_board = BOARDS[ith_win_index]

    ith_win_board[np.isin(ith_win_board, DRAWS[:ith_win_turn + 1])] = 0

    return ith_win_board.sum() * DRAWS[ith_win_turn]

def part_one():
    return score_ith_winner(0)

def part_two():
    return score_ith_winner(-1)

aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)
