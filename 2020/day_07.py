import aoc_helper
import re

raw = aoc_helper.day(7)

def parse_raw():
    bag_description = r"([a-z]+ [a-z]+) bags contain (.+)"
    formula = r"(\d+) ([a-z]+ [a-z]+) bag"
    bags = re.findall(bag_description, raw)
    return {bag: {description: int(n) for n, description in re.findall(formula, contents)} for bag, contents in bags}

formulas = parse_raw()
GOLD_BAG = "shiny gold"

def has_shiny(bag):
    if GOLD_BAG in formulas[bag]: return True
    return any(map(has_shiny, formulas[bag]))

def count(bag):
    return 1 + sum(n * count(inner) for inner, n in formulas[bag].items())

def part_one():
    return sum(map(has_shiny, formulas))

def part_two():
    return count(GOLD_BAG) - 1  # -1 since we don't count the GOLD_BAG itself!

print(part_one(), part_two())
aoc_helper.submit(7, part_one)
aoc_helper.submit(7, part_two)
