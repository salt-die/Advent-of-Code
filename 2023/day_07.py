import aoc_lube

HANDS = [
    (line[:5], int(line[5:])) for line in aoc_lube.fetch(year=2023, day=7).splitlines()
]


def score(hand):
    return sum(hand.count(c) for c in hand)


def score_wildcard(hand):
    if "J" in hand:
        return max(score_wildcard(hand.replace("J", c, 1)) for c in "23456789TQKA")
    return score(hand)


def tie_break(hand, ranks):
    return [ranks.index(card) for card in hand]


def winnings(ranks, scoring):
    scored = ((scoring(hand), tie_break(hand, ranks), bid) for hand, bid in HANDS)
    return sum(i * bid for i, (_, _, bid) in enumerate(sorted(scored), start=1))


def part_one():
    return winnings("23456789TJQKA", score)


def part_two():
    return winnings("J23456789TQKA", score_wildcard)


aoc_lube.submit(year=2023, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=7, part=2, solution=part_two)
