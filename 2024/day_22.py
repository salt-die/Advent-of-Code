from collections import Counter

import aoc_lube
from aoc_lube.utils import extract_ints, sliding_window

SECRET_NUMBERS = list(extract_ints(aoc_lube.fetch(year=2024, day=22)))


def next_secret_number(secret_number):
    secret_number ^= secret_number * 64
    secret_number %= 16777216
    secret_number ^= secret_number // 32
    secret_number %= 16777216
    secret_number ^= secret_number * 2048
    secret_number %= 16777216
    return secret_number


def nth_secret_number(secret_number):
    for _ in range(2000):
        secret_number = next_secret_number(secret_number)
    return secret_number


def buys(secret_number):
    for _ in range(2000):
        secret_number = next_secret_number(secret_number)
        yield secret_number % 10


def deltas(secret_number):
    deltas = set()
    for a, b, c, d, e in sliding_window(buys(secret_number), 5):
        delta = (b - a, c - b, d - c, e - d)
        if delta not in deltas:
            yield delta, e
            deltas.add(delta)


def part_one():
    return sum(nth_secret_number(secret_number) for secret_number in SECRET_NUMBERS)


def part_two():
    scores = Counter()
    for secret_number in SECRET_NUMBERS:
        for delta, buy in deltas(secret_number):
            scores[delta] += buy
    return max(scores.values())


aoc_lube.submit(year=2024, day=22, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=22, part=2, solution=part_two)
