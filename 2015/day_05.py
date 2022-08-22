import re

import aoc_helper

STRINGS = aoc_helper.day(5).splitlines()

def matches(string, *patterns):
    return all(
        bool(re.search(pattern, string))
        for pattern in patterns
    )

def part_one():
    return sum(
        matches(s, r"(.*[aeiou]){3}", r"(.)\1")
        and not matches(s, r"ab|cd|pq|xy")
        for s in STRINGS
    )

def part_two():
    return sum(
        matches(s, r"(..).*\1", r"(.).\1")
        for s in STRINGS
    )

aoc_helper.submit(5, part_one)
aoc_helper.submit(5, part_two)
