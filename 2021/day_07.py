
import numpy as np

import aoc_helper

RAW = aoc_helper.day(7)

CRAB_POSITIONS = np.fromiter(aoc_helper.utils.extract_ints(RAW), dtype=int)

def part_one():
    median = np.median(CRAB_POSITIONS).astype(int)
    return np.abs(CRAB_POSITIONS - median).sum(axis=-1)

def part_two():
    """
    Given:
        triangular(x) = x * (x + 1) / 2
        i in CRAB_POSITIONS
        n = len(CRAB_POSITONS)

    We need to minimize the following cost function:
        Cost(x) = Sum_i triangular(|x - i|) =>

        (Absolute values dropped as we approximate (x - i + 1) as (x - i) and the signs cancel.)
        Sum_i (x - i) * (x - i) / 2  =>
        Sum_i (x**2 - 2ix + i**2) / 2

    To minimize we use gradient descent. Take the derivative with respect to x and set to 0:
        0 = Sum_i x - i =>  0 = (Sum_i -i) + n * x
        x * n = Sum_i i  =>
        x = (Sum_i i) / n

    x is approximately the mean of the positions.
    """
    guess = np.mean(CRAB_POSITIONS).astype(int)
    guesses = np.arange(guess - 1, guess + 2)

    dif = np.abs(CRAB_POSITIONS - guesses[:, None])

    return (dif * (dif + 1) // 2).sum(-1).min()

aoc_helper.submit(7, part_one)
aoc_helper.submit(7, part_two)
