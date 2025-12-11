from functools import cache

import aoc_lube
import networkx as nx


def parse_raw():
    raw = aoc_lube.fetch(year=2025, day=11)
    lines = [line.partition(": ") for line in raw.splitlines()]
    return nx.DiGraph({node: neighbors.split() for node, _, neighbors in lines})


G = parse_raw()


def part_one():
    return len(list(nx.all_simple_paths(G, "you", "out")))


@cache
def npaths(node, seen):
    if node == "out":
        return seen == 2
    seen += node in {"fft", "dac"}
    return sum(npaths(neighbor, seen) for neighbor in G[node])


def part_two():
    return npaths("svr", 0)


aoc_lube.submit(year=2025, day=11, part=1, solution=part_one)
aoc_lube.submit(year=2025, day=11, part=2, solution=part_two)
