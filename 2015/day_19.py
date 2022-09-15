import re
from collections import defaultdict

import aoc_helper

sym_to_fruit = defaultdict(list("🍅🍇🍈🍉🍊🍋🍌🍍🍎🍐🍑🍒🍓🥑🥝🥭").pop)
raw_fruit = re.sub(r"[A-Z][a-z]*", lambda m: sym_to_fruit[m[0]], aoc_helper.day(19))
productions, FRUITS = raw_fruit.split("\n\n")

PRODUCE = defaultdict(list)
for a, b in re.findall(r"(.) => (.*)", productions):
    PRODUCE[a].append(b)

def part_one():
    return len({
        FRUITS[:i] + produce + FRUITS[i + 1:]
        for i, fruit in enumerate(FRUITS)
        for produce in PRODUCE[fruit]
    })

def part_two():
    return len(FRUITS) - 2 * FRUITS.count("🍒") - 2 * FRUITS.count("🍋") - 1

aoc_helper.submit(19, part_one)
aoc_helper.submit(19, part_two)
