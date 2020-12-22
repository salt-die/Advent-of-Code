from collections import deque
from itertools import islice

import aoc_helper
import numpy as np

raw = aoc_helper.day(22)
alice, bob = (deque(map(int, p.splitlines()[1:])) for p in raw.split("\n\n"))
enum = np.arange(len(alice) + len(bob), 0, -1)

def game(alice=alice, bob=bob, recurse=True):
    seen = set()
    while alice and bob and (s := (tuple(alice), tuple(bob))) not in seen:
        seen.add(s)

        a, b = alice.popleft(), bob.popleft()
        alice_wins = game(deque(islice(alice, a)), deque(islice(bob, b))) if recurse and a <= len(alice) and b <= len(bob) else a > b
        alice.extend((a, b)) if alice_wins else bob.extend((b, a))

    return bool(alice)

def part_one():
    game(recurse=False)
    return enum @ (alice or bob)

def part_two():
    game()
    return enum @ (alice or bob)

aoc_helper.submit(22, part_one)
aoc_helper.submit(22, part_two)
