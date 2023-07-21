from collections import deque
from functools import cache
from hashlib import md5
from itertools import count, islice
import re

import aoc_lube

SALT = aoc_lube.fetch(year=2016, day=14)

def find_repeat(n, hash_function):
    reg = re.compile(rf'(.)\1{{{n - 1}}}')
    for i in count():
        if m := reg.findall(hash_function(i)):
            yield i, m[0] if n == 3 else set(m)

def generate_keys(hash_function):
    quint_gen = find_repeat(5, hash_function)
    quints = deque()

    for index, repeated in find_repeat(3, hash_function):
        while not quints or quints[-1][0] < index + 1000:
            quints.append(next(quint_gen))

        while quints[0][0] <= index:
            quints.popleft()

        for quint_index, quint_repeats in quints:
            if quint_index > index + 1000:
                break

            if repeated in quint_repeats:
                yield index

def md5_hash(n):
    return md5(f"{SALT}{n}".encode()).hexdigest()

@cache
def stretched_hash(n):
    h = md5_hash(n)
    for _ in range(2016):
        h = md5(h.encode()).hexdigest()
    return h

def index_64(hash_function):
    return next(islice(generate_keys(hash_function), 63, None))

aoc_lube.submit(year=2016, day=14, part=1, solution=lambda: index_64(md5_hash))
aoc_lube.submit(year=2016, day=14, part=2, solution=lambda: index_64(stretched_hash))
