from collections import defaultdict
from functools import reduce
import re

import aoc_helper

raw = aoc_helper.day(21)

def parse_raw():
    ALLERGEN_RE = r"(.+) \(contains (.+)\)"
    foods = []
    contaminated = defaultdict(list)

    for ingredients, allergens in re.findall(ALLERGEN_RE, raw):
        ingredients = set(ingredients.split())
        foods.append(ingredients)
        for allergen in allergens.split(", "):
            contaminated[allergen].append(ingredients)
    return foods, {k: reduce(set.intersection, v) for k, v in contaminated.items()}

foods, allergens = parse_raw()

def part_one():
    safe = reduce(set.union, foods) - reduce(set.union, allergens.values())
    return sum(ingredient in safe for food in foods for ingredient in food)

def part_two():
    stack = list(allergens.items())
    canonical = []
    while stack:
        stack.sort(key=lambda tup: -len(tup[1]))
        allergen, (ingredient,) = stack.pop()
        canonical.append((allergen, ingredient))
        for _, possible in stack:
            possible.discard(ingredient)
    return ",".join(ingredient for _, ingredient in sorted(canonical))

aoc_helper.submit(21, part_one)
aoc_helper.submit(21, part_two)
