from collections import deque
from functools import reduce

import aoc_helper

DATA = aoc_helper.day(10).splitlines()

CLOSING = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CORRUPTED_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

INCOMPLETE_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

def syntax_scores(error):
    def tally(total, point):
        return 5 * total + point

    for line in DATA:
        close_queue = deque()

        for token in line:
            if token in CLOSING:
                close_queue.appendleft(CLOSING[token])
            elif close_queue[0] == token:
                close_queue.popleft()
            else:
                if error == "corrupted":
                    yield CORRUPTED_POINTS[token]
                break
        else:
            if error == "incomplete":
                yield reduce(tally, map(INCOMPLETE_POINTS.get, close_queue), 0)

def part_one():
     return sum(syntax_scores(error="corrupted"))

def part_two():
    scores = sorted(syntax_scores(error="incomplete"))
    return scores[len(scores) >> 1]

aoc_helper.submit(10, part_one)
aoc_helper.submit(10, part_two)
