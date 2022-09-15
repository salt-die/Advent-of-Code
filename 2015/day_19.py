import re
from collections import defaultdict

import aoc_helper


def parse_raw():
    symbol_to_fruit = defaultdict(list("🍅🍇🍈🍉🍊🍋🍌🍍🍎🍐🍑🍒🍓🥑🥝🥭").pop)
    def fruitize(match):
        return symbol_to_fruit[match.group(0)]

    raw = re.sub(r"([A-Z][a-z]*)", fruitize, aoc_helper.day(19))
    replacements, molecule = raw.split("\n\n")
    rules = {}
    for a, b in re.findall(r"(.*) => (.*)", replacements):
        rules.setdefault(a, []).append(b)

    return rules, molecule

RULES, MOLECULE = parse_raw()


def part_one():
    seen = set()
    for i, char in enumerate(MOLECULE):
        if subs := RULES.get(char):
            for sub in subs:
                seen.add(f"{MOLECULE[:i]}{sub}{MOLECULE[i + 1:]}")

    return len(seen)

def part_two():
    return len(MOLECULE) - 2 * MOLECULE.count("🍒") - 2 * MOLECULE.count("🍋") - 1

aoc_helper.submit(19, part_one)
aoc_helper.submit(19, part_two)
