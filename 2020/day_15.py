import aoc_helper

class SeparateLast(dict):
    def __init__(self):
        self.last = None
        super().__init__()

    def __setitem__(self, key, value):
        if self.last is not None:
            super().__setitem__(*self.last)
        self.last = key, value

raw = aoc_helper.day(15)
data = list(aoc_helper.extract_ints(raw))

def van_eck(nth):
    memory = SeparateLast()
    for i, n in enumerate(data):
        memory[n] = i

    for i in range(len(data), nth):
        n, pos = memory.last
        memory[(pos - memory[n]) if n in memory else 0] = i
    return memory.last[0]

def part_one():
    return van_eck(2020)

def part_two():
    return van_eck(30_000_000)

aoc_helper.submit(15, part_one)
aoc_helper.submit(15, part_two)
