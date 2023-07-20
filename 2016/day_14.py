from bisect import bisect_left
from functools import cache
from hashlib import md5
from itertools import count
import re

import aoc_lube

SALT = aoc_lube.fetch(year=2016, day=14)

def find_repeat(n, hash_function):
    reg = re.compile(rf'(.)\1{{{n - 1}}}')
    for i in count():
        if m := reg.findall(hash_function(i)):
            yield i, m[0]

def generate_keys(hash_function):
    quint_gen = find_repeat(5, hash_function)
    quints = []

    for index, repeated in find_repeat(3, hash_function):
        for i in count(bisect_left(quints, (index, "z"))):
            if i == len(quints):
                quints.append(next(quint_gen))

            quint_index, quint_repeated = quints[i]
            if quint_index > index + 1000:
                break
            if quint_repeated == repeated:
                yield index

def md5_hash(n):
    return md5(f"{SALT}{n}".encode()).hexdigest()

@cache
def stretched(n):
    h = md5_hash(n)
    for _ in range(2016):
        h = md5(h.encode()).hexdigest()
    return h

def part_one():
    for count, index in enumerate(generate_keys(md5_hash), start=1):
        if count == 64:
            return index

def part_two():
    for count, index in enumerate(generate_keys(stretched), start=1):
        if count == 64:
            return index

aoc_lube.submit(year=2016, day=14, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=14, part=2, solution=part_two)
