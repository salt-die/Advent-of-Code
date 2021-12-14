import re
from collections import Counter

import aoc_helper
from aoc_helper.utils import pairwise

def parse_raw():
    template, rules = aoc_helper.day(14).split("\n\n")

    return (
        template,
        {
            (a, b): ((a, c), (c, b))
            for (a, b), c in re.findall(r"(\w+) -> (\w)", rules)
        },
    )

TEMPLATE, RULES = parse_raw()

def apply_rules(n):
    pair_counts = Counter(pairwise(TEMPLATE))

    for _ in range(n):
        new_pairs = Counter()

        for pair, count in pair_counts.items():
            a, b = RULES[pair]

            new_pairs[a] += count
            new_pairs[b] += count

        pair_counts = new_pairs

    single_counts = Counter()

    for (a, b), count in pair_counts.items():
        single_counts[a] += count

    single_counts[TEMPLATE[-1]] += 1

    return max(single_counts.values()) - min(single_counts.values())

def part_one():
    return apply_rules(10)

def part_two():
    return apply_rules(40)

aoc_helper.submit(14, part_one)
aoc_helper.submit(14, part_two)
