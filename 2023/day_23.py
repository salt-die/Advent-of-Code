import aoc_lube
import networkx as nx
from aoc_lube.utils import extract_maze

GRID, G = extract_maze(aoc_lube.fetch(year=2023, day=23))
H, W = GRID.shape
START = 0, 1
END = H - 1, W - 2


def part_one():
    g = nx.DiGraph(G)
    slopes = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    for y, x in g.nodes:
        if GRID[y, x] in slopes:
            dy, dx = slopes[GRID[y, x]]
            g.remove_edge((y + dy, x + dx), (y, x))
    return max(len(path) for path in nx.all_simple_paths(g, START, END)) - 1


def part_two():
    # Edge contraction a la 2019, Day 18
    nx.set_edge_attributes(G, 1, name="weight")
    while True:
        for node, degree in nx.degree(G):
            if degree == 1 and node != START and node != END:
                G.remove_node(node)
                break
            if degree == 2:
                (*_, w1), (*_, w2) = G.edges(node, data="weight")
                G.add_edge(*G.neighbors(node), weight=w1 + w2)
                G.remove_node(node)
                break
        else:
            break

    return max(
        nx.path_weight(G, path, weight="weight")
        for path in nx.all_simple_paths(G, START, END)
    )


aoc_lube.submit(year=2023, day=23, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=23, part=2, solution=part_two)
