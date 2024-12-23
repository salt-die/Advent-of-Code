import aoc_lube
import networkx as nx

G = nx.Graph(line.split("-") for line in aoc_lube.fetch(year=2024, day=23).splitlines())


def part_one():
    total = 0
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) < 3:
            continue
        elif len(clique) > 3:
            return total

        total += any(u.startswith("t") for u in clique)


def part_two():
    return ",".join(sorted(nx.max_weight_clique(G, None)[0]))


aoc_lube.submit(year=2024, day=23, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=23, part=2, solution=part_two)
