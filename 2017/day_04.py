import aoc_lube

PASS_PHRASES = aoc_lube.fetch(year=2017, day=4).split("\n")


def all_unique(words):
    return len(set(words)) == len(words)


def valid_phrases(cmp):
    return sum(all_unique(cmp(pass_phrase.split())) for pass_phrase in PASS_PHRASES)


def part_one():
    return valid_phrases(lambda words: words)


def part_two():
    return valid_phrases(lambda words: [frozenset(word) for word in words])


aoc_lube.submit(year=2017, day=4, part=1, solution=part_one)
aoc_lube.submit(year=2017, day=4, part=2, solution=part_two)
