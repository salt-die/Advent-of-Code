import aoc_lube
import networkx as nx


def parse_raw():
    for line in aoc_lube.fetch(year=2023, day=25).replace(":", " ").splitlines():
        node, *neighbors = line.split()
        yield node, neighbors


G = nx.Graph(dict(parse_raw()))


def part_one():
    G.remove_edges_from(nx.minimum_edge_cut(G))
    a, b = nx.connected_components(G)
    return len(a) * len(b)


aoc_lube.submit(year=2023, day=25, part=1, solution=part_one)
