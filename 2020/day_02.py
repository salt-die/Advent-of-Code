import aoc_helper
import re

raw = aoc_helper.day(2)

def parse_raw():
    pattern = r'(\d+)-(\d+) (\w): (\w+)'
    return re.findall(pattern, raw)

data = parse_raw()

def part_one():
    return sum(int(mi) <= pw.count(letter) <= int(mx) for mi, mx, letter, pw in data)

def part_two():
    return sum((pw[int(mi) - 1] == letter) ^ (pw[int(mx) - 1] == letter) for mi, mx, letter, pw in data)

aoc_helper.submit(day=2, solv_func=part_one)
aoc_helper.submit(day=2, solv_func=part_two)
