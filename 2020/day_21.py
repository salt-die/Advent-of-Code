from collections import defaultdict
import re

import aoc_helper
import networkx as nx

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
    return foods, {k: set.intersection(*v) for k, v in contaminated.items()}

foods, allergens = parse_raw()

def part_one():
    safe = set.union(*foods) - set.union(*allergens.values())
    return sum(ingredient in safe for food in foods for ingredient in food)

def part_two():
    G = nx.from_dict_of_lists(allergens)
    canonical = sorted(nx.bipartite.maximum_matching(G).items())
    return ",".join(ingredient for allergen, ingredient in canonical if allergen in allergens)

aoc_helper.submit(21, part_one)
aoc_helper.submit(21, part_two)
