import aoc_helper
from aoc_helper.utils import ilen

def look_and_say(it):
    curr = next(it)
    count = 1

    for i in it:
        if i != curr:
            yield count
            yield curr

            curr = i
            count = 1
        else:
            count += 1

    yield count
    yield curr

def len_nth_look(n):
    it = iter(map(int, aoc_helper.day(10)))
    for _ in range(n):
        it = look_and_say(it)
    return ilen(it)

def part_one():
    return len_nth_look(40)

def part_two():
    return len_nth_look(50)

aoc_helper.submit(10, part_one)
aoc_helper.submit(10, part_two)
