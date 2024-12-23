from hashlib import md5
from heapq import heappop, heappush

import aoc_lube
from aoc_lube.utils import Vec2

PASSCODE = aoc_lube.fetch(year=2016, day=17)
DIRS = (-1, 0), (1, 0), (0, -1), (0, 1)


def bfs(shortest=True):
    heap = [(0, "", Vec2(0, 0))]
    while heap:
        length, path, pos = heappop(heap)
        if pos == (3, 3):
            if shortest:
                return path
            longest_path = path
            continue

        for code, door, dir in zip(
            md5((PASSCODE + path).encode()).hexdigest(), "UDLR", DIRS
        ):
            if code > "a" and (pos + dir).inbounds((4, 4)):
                heappush(heap, (length + 1, path + door, pos + dir))
    return longest_path


def part_one():
    return bfs()


def part_two():
    return len(bfs(False))


aoc_lube.submit(year=2016, day=17, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=17, part=2, solution=part_two)
