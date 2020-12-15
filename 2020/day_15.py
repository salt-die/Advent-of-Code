import aoc_helper

raw = aoc_helper.day(15)
data = list(aoc_helper.extract_ints(raw))

def van_eck(nth):
    memory = {}
    it = iter(data)
    last = next(it)
    for i, n in enumerate(it, start=1):
        memory[last], last = i, n

    for i in range(len(data), nth):
        memory[last], last = i, i - memory[last] if last in memory else 0
    return last

def part_one():
    return van_eck(2020)

def part_two():
    return van_eck(30_000_000)

aoc_helper.submit(15, part_one)
aoc_helper.submit(15, part_two)
