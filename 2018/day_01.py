import aoc_lube

FREQUENCIES = [eval(n) for n in aoc_lube.fetch(year=2018, day=1).split()]


def part_one():
    return sum(FREQUENCIES)


def part_two():
    seen = set()
    total = 0
    while True:
        for frequency in FREQUENCIES:
            if total in seen:
                return total
            seen.add(total)
            total += frequency


aoc_lube.submit(year=2018, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2018, day=1, part=2, solution=part_two)
