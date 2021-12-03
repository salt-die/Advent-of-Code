import numpy as np

import aoc_helper

RAW = aoc_helper.day(3)
DATA = np.array([list(map(int, line)) for line in RAW.splitlines()])
h, w = DATA.shape

BIN_POWERS = np.geomspace(2**(w - 1), 1, w, dtype=int)

def part_one():
    gamma_digits = DATA.sum(axis=0) > h >> 1

    gamma = gamma_digits @ BIN_POWERS
    episilon = ~gamma_digits @ BIN_POWERS

    return gamma * episilon

def part_two():
    oxy_rating = co2_rating = DATA

    for i in range(w):
        if half_sum := len(oxy_rating) >> 1:
            mask = oxy_rating[:, i]
            oxy_rating = oxy_rating[mask == (mask.sum() >= half_sum)]

        if half_sum := len(co2_rating) >> 1:
            mask = co2_rating[:, i] == 0
            co2_rating = co2_rating[mask == (mask.sum() <= half_sum)]

    oxy_rating = oxy_rating[0] @ BIN_POWERS
    co2_rating = co2_rating[0] @ BIN_POWERS

    return oxy_rating * co2_rating

aoc_helper.submit(3, part_one)
aoc_helper.submit(3, part_two)
