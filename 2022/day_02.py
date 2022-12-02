import aoc_lube

strats = dict(
    A=0, B=1, C=2,
    X=0, Y=1, Z=2,
)

games = [
    (strats[a], strats[b])
    for a, _, b in aoc_lube.fetch(year=2022, day=2).splitlines()
]

def part_one():
    return sum(b + 1 + 3 * ((b - a + 1) % 3) for a, b in games)

def part_two():
    return sum((b - 1 + a) % 3 + 1 + 3 * b for a, b in games)

aoc_lube.submit(year=2022, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=2, part=2, solution=part_two)
