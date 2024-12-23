import aoc_lube
import networkx as nx

G = nx.Graph(line.split("-") for line in aoc_lube.fetch(year=2024, day=23).splitlines())


def part_one():
    return sum(
        len(clique) == 3 and any(u.startswith("t") for u in clique)
        for clique in nx.enumerate_all_cliques(G)
    )


def part_two():
    return ",".join(sorted(max(nx.find_cliques(G), key=len)))


aoc_lube.submit(year=2024, day=23, part=1, solution=part_one)
aoc_lube.submit(year=2024, day=23, part=2, solution=part_two)
