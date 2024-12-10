import aoc_lube
import networkx as nx
from aoc_lube.utils import grid_steps, ilen


def parse_raw():
    grid = aoc_lube.fetch(year=2024, day=10).splitlines()
    trailheads = []
    summits = []
    G = nx.DiGraph()
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == "0":
                trailheads.append((y, x))
            elif char == "9":
                summits.append((y, x))
            G.add_node((y, x), value=int(char))

    nodes = G.nodes(data="value")
    for a, b in grid_steps(4, len(grid), len(grid[0])):
        if nodes[b] - nodes[a] == 1:
            G.add_edge(a, b)
    return G, trailheads, summits


G, TRAILHEADS, SUMMITS = parse_raw()


def part_one():
    return sum(nx.has_path(G, a, b) for a in TRAILHEADS for b in SUMMITS)


def part_two():
    return sum(
        ilen(
            nx.all_simple_edge_paths(G, a, b)
            for a in TRAILHEADS
            for b in SUMMITS
            if nx.has_path(G, a, b)
        )
    )


aoc_lube.submit(year=2024, day=10, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=10, part=2, solution=part_two)
