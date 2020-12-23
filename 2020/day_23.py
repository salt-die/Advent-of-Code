import aoc_helper


class Block:
    def __init__(self, val):
        self.val = val

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self._r = value
        self._r.l = self


class Linked:
    head = None
    blocks = {}

    def __init__(self, iterable):
        self.extend(iterable)

    def append(self, value):
        block = self.blocks[value] = Block(value) # Fast look up of blocks by value

        if self.head is None:
            self.head = self.current = block
        else:
            self.tail.r = block
            block.r = self.head

        self.tail = block

    def next(self, until=None):
        while True:
            self.current = self.current.r
            if until is None or until == self.current.l.val:
                return self.current.l.val

    def extend(self, iterable):
        for i in iterable:
            self.append(i)


def move(n):
    for _ in range(n):
        cur = cups.current
        next_3 = first, m, last = cur.r, cur.r.r, cur.r.r.r
        vals = first.val, m.val, last.val

        cur.r = last.r

        dest = cups.next() - 1 or len(cups.blocks)
        while dest in vals:
            dest = dest - 1 or len(cups.blocks)
        dest = cups.blocks[dest]

        last.r = dest.r
        dest.r = first

def part_one():
    move(100)
    cups.next(1)
    return "".join(str(cups.next()) for _ in range(len(cups.blocks) - 1))

def part_two():
    cups.extend(range(10, 1_000_001))
    move(10_000_000)
    cups.next(1)
    return cups.next() * cups.next()

raw = aoc_helper.day(23)
cups = Linked(map(int, raw))

aoc_helper.submit(23, part_one)
aoc_helper.submit(23, part_two)
