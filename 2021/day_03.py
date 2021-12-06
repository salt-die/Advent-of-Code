from operator import ge, le

import numpy as np

import aoc_helper

RAW = aoc_helper.day(3)
DATA = np.array([list(map(int, line)) for line in RAW.splitlines()])
h, w = DATA.shape

BIN_POWERS = 2**np.arange(w)[::-1]

def part_one():
    """
    A fun alternate way of getting gamma is to run the "traffic" cellular automata
    on the data to sort all the bits. Then gamma is the middle array.

    The evolution of this automata on a 1d array over time looks like:
    ```
    t = 0: [1 0 0 1 0 1 1 1 0 1]
    t = 1: [1 0 1 0 1 0 1 1 1 0]
    t = 2: [1 1 0 1 0 1 0 1 1 0]
    t = 3: [1 1 1 0 1 0 1 0 1 0]
    t = 4: [1 1 1 1 0 1 0 1 0 0]
    t = 5: [1 1 1 1 1 0 1 0 0 0]
    t = 6: [1 1 1 1 1 1 0 0 0 0]
    ```
    All the ones shuffle to one side and the zeros to the other.
    The state diagram is:
        000 001 010 011 100 101 110 111
         0   1   0   0   0   1   1   1

    Or symbolically:
        X0Y X1Y
         Y   X

    A possible implementation:
    ```
    from scipy.ndimage import convolve

    KERNEL = np.array([[0], [0], [1]])

    def step(universe):
        return np.where(
            universe,
            convolve(universe, KERNEL),
            convolve(universe, KERNEL[::-1]),
        )

    universe = DATA

    while (universe != (universe := step(universe))).any():
        pass

    gamma = universe[h // 2] @ BIN_POWERS
    ```
    """
    gamma_digits = DATA.sum(axis=0) > h >> 1

    gamma = gamma_digits @ BIN_POWERS
    epsilon = ~gamma_digits @ BIN_POWERS

    return gamma * epsilon

def gas_filter(mask_bit, cmp):
    ratings = DATA

    for i in range(w):
        if half_sum := len(ratings) >> 1:
            mask = ratings[:, i] == mask_bit
            ratings = ratings[mask == cmp(mask.sum(), half_sum)]

    return ratings[0]

def part_two():
    oxy_rating = gas_filter(1, ge) @ BIN_POWERS
    co2_rating = gas_filter(0, le) @ BIN_POWERS

    return oxy_rating * co2_rating

aoc_helper.submit(3, part_one)
aoc_helper.submit(3, part_two)
