import aoc_lube
import numpy as np

def parse_input():
    dirs = dict(D=(1, 0), U=(-1, 0), L=(0, -1), R=(0, 1))
    for line in aoc_lube.fetch(year=2022, day=9).splitlines():
        d, n = line.split()
        yield dirs[d], int(n)

def simulate_rope(nknots):
    rope = np.zeros((nknots, 2), int)
    seen = {(0, 0)}
    for d, n in parse_input():
        for _ in range(n):
            rope[0] += d
            for i in range(nknots - 1):
                delta = rope[i] - rope[i + 1]
                rope[i + 1] += np.sign(delta) * (np.linalg.norm(delta, ord=np.inf) > 1)
            seen.add(tuple(rope[-1]))
    return len(seen)

def part_one():
    return simulate_rope(2)

def part_two():
    return simulate_rope(10)

aoc_lube.submit(year=2022, day=9, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=9, part=2, solution=part_two)
