from collections import Counter

import aoc_lube

RAW = aoc_lube.fetch(year=2025, day=7)
START = RAW.index("S")
SPLITTERS = [i for row in RAW.splitlines() for i, char in enumerate(row) if char == "^"]


def part_one():
    nsplits, beams = 0, {START}
    for splitter in SPLITTERS:
        if splitter in beams:
            nsplits += 1
            beams.remove(splitter)
            beams.update((splitter - 1, splitter + 1))
    return nsplits


def part_two():
    beams = Counter({START: 1})
    for splitter in SPLITTERS:
        if splitter in beams:
            count = beams.pop(splitter)
            beams[splitter - 1] += count
            beams[splitter + 1] += count
    return beams.total()


aoc_lube.submit(year=2025, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=7, part=2, solution=part_two)
