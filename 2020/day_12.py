import aoc_helper
import re

raw = aoc_helper.day(12)

def parse_raw():
    pattern = re.compile(r"([NEWSLRF])(\d+)")
    return [(dir_, int(val)) for dir_, val in pattern.findall(raw)]

data = parse_raw()

cards = dict(zip("NEWS", (1j, 1, -1, -1j)))
turns = dict(zip("LR", (1j, -1j)))

def part_one():
    facing = 1 + 0j
    loc = 0 + 0j
    for dir_, val in data:
        if dir_ in cards:
            loc += cards[dir_] * val
        elif dir_ in turns:
            facing *= turns[dir_] ** (val // 90)
        elif dir_ == "F":
            loc += facing * val
    return round(abs(loc.real) + abs(loc.imag))

def part_two():
    wp = 10 + 1j
    loc = 0 + 0j
    for dir_, val in data:
        if dir_ in cards:
            wp += cards[dir_] * val
        elif dir_ in turns:
            wp *= turns[dir_] ** (val // 90)
        elif dir_ == "F":
            loc += wp * val
    return round(abs(loc.real) + abs(loc.imag))

aoc_helper.submit(12, part_one)
aoc_helper.submit(12, part_two)
