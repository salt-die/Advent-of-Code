import aoc_helper


class Linked:
    current = None
    blocks = {}

    def __init__(self, iterable):
        self.extend(iterable)

    def append(self, value):
        block = self.blocks[value] = type('', (), {"val": value})()  # Fast look up of blocks by value; vals are all unique

        if self.current is None:
            self.current = block
        else:
            self.tail.r = block

        block.r = self.current
        self.tail = block

    def next(self, until=None):
        while val := self.current.val:  # All vals are truth-y
            self.current = self.current.r
            if until is None or until == val:
                return val

    def extend(self, iterable):
        for i in iterable: self.append(i)


def move(n):
    for _ in range(n):
        cur = cups.current
        head, cur.r = cur.r, cur.r.r.r.r

        dest = cups.next() - 1 or len(cups.blocks)
        while dest in (head.val, head.r.val, head.r.r.val):
            dest = dest - 1 or len(cups.blocks)
        dest = cups.blocks[dest]

        dest.r, head.r.r.r = head, dest.r

def part_one():
    move(100)
    cups.next(until=1)
    return "".join(str(cups.next()) for _ in range(len(cups.blocks) - 1))

def part_two():
    cups.extend(range(10, 1_000_001))
    move(10_000_000)
    cups.next(until=1)
    return cups.next() * cups.next()

raw = aoc_helper.day(23)
cups = Linked(map(int, raw))

aoc_helper.submit(23, part_one)
aoc_helper.submit(23, part_two)
