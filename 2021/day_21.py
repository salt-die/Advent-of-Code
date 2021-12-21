from collections import Counter
from functools import cache
from itertools import product
from typing import NamedTuple

import aoc_helper
from aoc_helper.utils import shiftmod


class GameState(NamedTuple):
    pos_0: int=9
    pos_1: int=4

    score_0: int=0
    score_1: int=0

    turn: int=0

    def move(self, n):
        pos_0, pos_1, score_0, score_1, turn = self

        if turn % 2 == 0:
            pos_0 = shiftmod(pos_0 + n, 10)
            score_0 += pos_0
        else:
            pos_1 = shiftmod(pos_1 + n, 10)
            score_1 += pos_1

        return GameState(pos_0, pos_1, score_0, score_1, turn + 1)

def part_one():
    gamestate = GameState()

    while max(gamestate.score_0, gamestate.score_1) < 1000:
        gamestate = gamestate.move(9 * gamestate.turn + 6)

    return min(gamestate.score_0, gamestate.score_1) * 3 * gamestate.turn

def part_two():
    FREQUENCIES = Counter(map(sum, product((1, 2, 3), repeat=3)))

    @cache
    def play(gamestate):
        if gamestate.score_0 >= 21:
            return 1

        if gamestate.score_1 >= 21:
            return 1j

        return sum(freq * play(gamestate.move(n)) for n, freq in FREQUENCIES.items())

    wins = play(GameState())

    return max(int(wins.real), int(wins.imag))

aoc_helper.submit(21, part_one)
aoc_helper.submit(21, part_two)
