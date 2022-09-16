from itertools import count

import numpy as np
from sympy.ntheory import divisor_sigma, divisors

import aoc_helper

N = int(aoc_helper.day(20))
STEP = 360

def least_n(target):
    """
    Find the least n such that::
        target < np.e ** np.euler_gamma * n * np.log(np.log(n))

    See: https://en.wikipedia.org/wiki/Divisor_function (Robin's Theorem)
    """
    E_GAMMA = np.e ** np.euler_gamma

    min = 5041  # Min value that theorem is valid.
    max = target

    while min != max:
        mid = (min + max) // 2

        if E_GAMMA * mid * np.log(np.log(mid)) < target:
            min = mid + 1
        else:
            max = mid

    return min - min % STEP  # Return a multiple of STEP. STEP has lots of small prime divisors.


def part_one():
    target = N // 10
    for i in count(least_n(target), STEP):
        if divisor_sigma(i) >= target:
            return i

def part_two():
    target = N // 11
    for i in count(least_n(target), STEP):  # Robin's Theorem will still be good enough for a lower bound.
        if sum(p for p in divisors(i) if i // p <= 50) >= target:
            return i

aoc_helper.submit(20, part_one)
aoc_helper.submit(20, part_two)
