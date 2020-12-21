from collections import defaultdict
from functools import reduce
import re

import aoc_helper

raw = aoc_helper.day(21)

def parse_raw():
    ALLERGEN_RE = r"(.+) \(contains (.+)\)"
    foods = []
    allergen_to_ingredients = defaultdict(list)

    for ingredients, allergens in re.findall(ALLERGEN_RE, raw):
        ingredients = set(ingredients.split())
        foods.append(ingredients)
        for allergen in allergens.split(", "):
            allergen_to_ingredients[allergen].append(ingredients)
    return foods, {allergen: reduce(set.intersection, ingredients) for allergen, ingredients in allergen_to_ingredients.items()}

foods, allergens = parse_raw()

def part_one():
    safe_ingredients = reduce(set.union, foods) - reduce(set.union, allergens.values())
    return sum(ingredient in safe_ingredients for food in foods for ingredient in food)

def part_two():
    stack = sorted(allergens.items(), key=lambda tup: -len(tup[1]))
    canonical = []
    while stack:
        allergen, (ingredient,) = stack.pop()
        canonical.append((allergen, ingredient))
        for _, possible in stack:
            possible.discard(ingredient)
        stack.sort(key=lambda tup: -len(tup[1]))
    return ",".join(ingredient for _, ingredient in sorted(canonical, key=lambda tup: tup[0]))

aoc_helper.submit(21, part_one)
aoc_helper.submit(21, part_two)
