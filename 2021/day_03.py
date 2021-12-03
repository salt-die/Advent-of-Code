from operator import ge, le

import numpy as np

import aoc_helper

RAW = aoc_helper.day(3)
DATA = np.array([list(map(int, line)) for line in RAW.splitlines()])
h, w = DATA.shape

BIN_POWERS = 2**np.arange(w)[::-1]

def part_one():
    gamma_digits = DATA.sum(axis=0) > h >> 1

    gamma = gamma_digits @ BIN_POWERS
    episilon = ~gamma_digits @ BIN_POWERS

    return gamma * episilon

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
