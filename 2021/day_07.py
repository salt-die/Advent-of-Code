
from statistics import median, mean

import aoc_helper

RAW = aoc_helper.day(7)

CRAB_POSITIONS = tuple(aoc_helper.utils.extract_ints(RAW))

def fuel_cost(p, cost_function):
    """
    Return total cost of fuel to move each crab to p given a cost_function.
    """
    return sum(
        cost_function(abs(i - p))
        for i in CRAB_POSITIONS
    )

def part_one():
    return fuel_cost(
        int(median(CRAB_POSITIONS)),
        lambda x: x,
    )

def triangular(x):
    return x * (x + 1) // 2

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
    guess = int(mean(CRAB_POSITIONS))

    return min(
        fuel_cost(m, triangular)
        for m in range(guess - 1, guess + 2)
    )

aoc_helper.submit(7, part_one)
aoc_helper.submit(7, part_two)
