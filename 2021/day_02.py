import re

import aoc_helper

RAW = aoc_helper.day(2)
DATA = [
    (direction, int(amount))
    for direction, amount in re.findall(r"(\w+) (\d+)", RAW)
]

def part_one():
    depth = x = 0

    for direction, amount in DATA:
        match direction:
            case "forward":
                x += amount
            case "down":
                depth += amount
            case "up":
                depth -= amount

    return depth * x

def part_two():
    depth = x = aim = 0

    for direction, amount in DATA:
        match direction:
            case "forward":
                x += amount
                depth += aim * amount
            case "down":
                aim += amount
            case "up":
                aim -= amount

    return depth * x

aoc_helper.submit(2, part_one)
aoc_helper.submit(2, part_two)
