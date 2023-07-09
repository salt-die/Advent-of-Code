from math import prod

import aoc_lube
from parse import parse

def process():
    outputs, held, seen, processing = {}, {}, {}, []

    def add_value(value, bot):
        held.setdefault(bot, []).append(value)
        seen.setdefault(bot, set()).add(value)
        if len(held[bot]) == 2:
            processing.append(bot)

    for line in aoc_lube.fetch(year=2016, day=10).splitlines():
        if match := parse("{} gives low to {} and high to {}", line):
            bot, *output = match
            outputs[bot] = output
        elif match := parse("value {:d} goes to {}", line):
            add_value(*match)

    while processing:
        bot = processing.pop()
        for value, out in zip(sorted(held.pop(bot)), outputs[bot]):
            add_value(value, out)

    return seen

SEEN = process()

def part_one():
    for bot, processed in SEEN.items():
        if processed == {17, 61}:
            return bot[4:]

def part_two():
    return prod(SEEN[f"output {n}"].pop() for n in range(3))

aoc_lube.submit(year=2016, day=10, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=10, part=2, solution=part_two)
