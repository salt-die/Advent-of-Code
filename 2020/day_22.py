from collections import deque
from itertools import islice

import aoc_helper
import numpy as np

raw = aoc_helper.day(22)

def parse_raw():
    alice, bob = raw.split("\n\n")
    return deque(map(int, alice.splitlines()[1:])), deque(map(int, bob.splitlines()[1:]))

alice, bob = parse_raw()
enum = np.arange(len(alice) + len(bob), 0, -1)

def part_one():
    while alice and bob:
        a, b = alice.popleft(), bob.popleft()
        alice.extend((a, b)) if a > b else bob.extend((b, a))

    return enum @ (alice or bob)

def game(alice=alice, bob=bob):
    seen = set()
    while alice and bob:
        if (s := (tuple(alice), tuple(bob))) in seen:
            return True
        seen.add(s)

        a, b = alice.popleft(), bob.popleft()
        if a <= len(alice) and b <= len(bob):
            sub_alice, sub_bob = deque(islice(alice, a)), deque(islice(bob, b))
            alice.extend((a, b)) if game(sub_alice, sub_bob) else bob.extend((b, a))
        else:
            alice.extend((a, b)) if a > b else bob.extend((b, a))

    return bool(alice)

def part_two():
    game(); return enum @ (alice or bob)

aoc_helper.submit(22, part_one)
aoc_helper.submit(22, part_two)
