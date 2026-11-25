from string import ascii_lowercase

import aoc_lube

RAW = aoc_lube.fetch(year=2018, day=5)


def react(polymer: str) -> int:
    stack = []
    for unit in polymer:
        if stack and abs(ord(stack[-1]) - ord(unit)) == 32:
            stack.pop()
        else:
            stack.append(unit)
    return len(stack)


def part_one():
    return react(RAW)


def part_two():
    return min(
        react(RAW.replace(unit, "").replace(unit.upper(), ""))
        for unit in ascii_lowercase
    )


aoc_lube.submit(year=2018, day=5, part=1, solution=part_one)
aoc_lube.submit(year=2018, day=5, part=2, solution=part_two)
