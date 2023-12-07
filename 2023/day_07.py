import aoc_lube

HANDS = [
    (line[:5].translate(str.maketrans("TJQKA", "ABCDE")), int(line[5:]))
    for line in aoc_lube.fetch(year=2023, day=7).splitlines()
]


def score(hand):
    return sum(hand.count(c) for c in hand)


def score_wildcard(hand):
    return max(score(hand.replace("B", c)) for c in "23456789ACDE")


def part_one():
    scored = ((score(hand), int(hand, 16), bid) for hand, bid in HANDS)
    return sum(i * bid for i, (_, _, bid) in enumerate(sorted(scored), start=1))


def part_two():
    scored = (
        (score_wildcard(hand), int(hand.replace("B", "1"), 16), bid)
        for hand, bid in HANDS
    )
    return sum(i * bid for i, (_, _, bid) in enumerate(sorted(scored), start=1))


aoc_lube.submit(year=2023, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=7, part=2, solution=part_two)
