from collections import deque

import aoc_lube

N = int(aoc_lube.fetch(year=2016, day=13))

def is_open(x, y):
    return (x**2 + 3 * x + 2 * x * y + y + y**2 + N).bit_count() % 2 == 0

def bfs():
    queue = deque([(1, 1, 0)])
    seen = set()
    while queue:
        x, y, n = queue.popleft()

        if 0 <= x and 0 <= y and (x, y) not in seen and is_open(x, y):
            seen.add((x, y))
            queue.append((x + 1, y, n + 1))
            queue.append((x, y + 1, n + 1))
            queue.append((x - 1, y, n + 1))
            queue.append((x, y - 1, n + 1))
            yield x, y, n

def part_one():
    for x, y, n in bfs():
        if (x, y) == (31, 39):
            return n

def part_two():
    for i, (_, _, n) in enumerate(bfs()):
        if n > 50:
            return i

aoc_lube.submit(year=2016, day=13, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=13, part=2, solution=part_two)
