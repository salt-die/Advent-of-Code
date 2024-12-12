import aoc_lube
from aoc_lube.utils import UnionFind, Vec2


def regions():
    grid = {}

    for y, line in enumerate(aoc_lube.fetch(year=2024, day=12).splitlines()):
        for x, char in enumerate(line):
            grid[Vec2(y, x)] = char

    uf = UnionFind(grid)
    for pos, char in grid.items():
        for adj in pos.adj():
            if grid.get(adj) == char:
                uf.merge(pos, adj)
    return uf.components


def perimeter(region):
    return 4 * len(region) - sum(adj in region for pos in region for adj in pos.adj())


def nsides(region):
    total = 0
    for dir in Vec2(0, 0).adj():
        edge_uf = UnionFind(pos for pos in region if pos + dir not in region)
        for pos in edge_uf:
            if (adj := pos + dir.rotate(True)) in edge_uf:
                edge_uf.merge(pos, adj)
            if (adj := pos + dir.rotate(False)) in edge_uf:
                edge_uf.merge(pos, adj)
        total += len(edge_uf)
    return total


def part_one():
    return sum(len(region) * perimeter(region) for region in regions())


def part_two():
    return sum(len(region) * nsides(region) for region in regions())


aoc_lube.submit(year=2024, day=12, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=12, part=2, solution=part_two)
