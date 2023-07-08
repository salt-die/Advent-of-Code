from itertools import takewhile, islice

import aoc_lube
from aoc_lube.utils import ilen

DATA = aoc_lube.fetch(year=2016, day=9)

def consume_int(it):
    return int("".join(takewhile(str.isdigit, it)) or 0)

def iter_markers(data):
    it = iter(data)
    if pre := ilen(takewhile(lambda char: char != "(", it)):
        yield -1, pre
    elif consume := consume_int(it):
        yield consume_int(it), "".join(islice(it, consume))
        yield from iter_markers(it)

def decompress_len_v1(data):
    for repeat, consume in iter_markers(data):
        yield consume if repeat == -1 else len(consume) * repeat

def decompress_len_v2(data):
    for repeat, consume in iter_markers(data):
        yield consume if repeat == -1 else sum(decompress_len_v2(consume)) * repeat

def part_one():
    return sum(decompress_len_v1(DATA))

def part_two():
    return sum(decompress_len_v2(DATA))

aoc_lube.submit(year=2016, day=9, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=9, part=2, solution=part_two)
