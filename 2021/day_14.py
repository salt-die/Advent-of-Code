import re
from collections import Counter

import aoc_helper
from aoc_helper.utils import pairwise

def parse_raw():
    template, rules = aoc_helper.day(14).split("\n\n")

    return template, {tuple(k): v for k, v in re.findall(r"(\w+) -> (\w)", rules)}

TEMPLATE, RULES = parse_raw()

def apply_rules(n):
    pair_counts = Counter(pairwise(TEMPLATE))

    for _ in range(n):
        new_pairs = Counter()

        for pair in pair_counts:
            a, b = pair

            c = RULES[pair]
            pair_count = pair_counts[pair]

            new_pairs[a, c] += pair_count
            new_pairs[c, b] += pair_count

        pair_counts = new_pairs

    single_counts = Counter()

    for a, b in pair_counts:
        single_counts[a] += pair_counts[a, b]

    single_counts[TEMPLATE[-1]] += 1

    return max(single_counts.values()) - min(single_counts.values())

def part_one():
    return apply_rules(10)

def part_two():
    return apply_rules(40)

aoc_helper.submit(14, part_one)
aoc_helper.submit(14, part_two)
