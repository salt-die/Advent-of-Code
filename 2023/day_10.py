from typing import NamedTuple

import aoc_lube
import networkx as nx


class Point(NamedTuple):
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)


DIRS = [N, E, S, W] = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]
Δs = {"|": (N, S), "J": (N, W), "L": (N, E), "7": (S, W), "F": (S, E), "-": (W, E)}


def parse_raw():
    grid = [list(line) for line in aoc_lube.fetch(year=2023, day=10).splitlines()]
    yield grid

    edges = set()
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            pos = Point(y, x)
            if char in Δs:
                Δ1, Δ2 = Δs[char]
                edges.add((pos, pos + Δ1))
                edges.add((pos, pos + Δ2))
            elif char == "S":
                start = pos
                for Δ in DIRS:
                    edges.add((pos, pos + Δ))

    for pipe, (Δ1, Δ2) in Δs.items():
        if (start + Δ1, start) in edges and (start + Δ2, start) in edges:
            grid[start.y][start.x] = pipe
            break

    H = nx.Graph(((u, v) for u, v in edges if (v, u) in edges))
    for component in nx.connected_components(H):
        if start in component:
            yield component
            return


GRID, PIPES = parse_raw()


def part_one():
    return len(PIPES) // 2


def part_two():
    ntiles = 0
    for y, line in enumerate(GRID):
        inside = False
        for x, pipe in enumerate(line):
            if (y, x) not in PIPES:
                ntiles += inside
            elif pipe in "|F7":
                inside = not inside
    return ntiles


aoc_lube.submit(year=2023, day=10, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=10, part=2, solution=part_two)
