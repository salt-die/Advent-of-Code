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
    seen = set()
    for i, char in enumerate(FRUITS):
        if subs := PRODUCE.get(char):
            for sub in subs:
                seen.add(f"{FRUITS[:i]}{sub}{FRUITS[i + 1:]}")

    return len(seen)

def part_two():
    return len(FRUITS) - 2 * FRUITS.count("🍒") - 2 * FRUITS.count("🍋") - 1

aoc_helper.submit(19, part_one)
aoc_helper.submit(19, part_two)
