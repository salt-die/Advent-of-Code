import aoc_lube

N, E, S, W = -1j, 1, 1j, -1
Δs = {
    "|": (N, S),
    "J": (N, W),
    "L": (N, E),
    "7": (S, W),
    "F": (S, E),
    "-": (W, E),
    "S": (N, E, S, W),
    ".": (),
}


def parse_raw():
    grid = {}
    edges = set()
    for y, line in enumerate(aoc_lube.fetch(year=2023, day=10).splitlines()):
        for x, char in enumerate(line):
            pos = complex(x, y)
            grid[pos] = char
            for Δ in Δs[char]:
                edges.add((pos, pos + Δ))

            if char == "S":
                cycle = {pos}
                stack = [pos]

    yield y + 1, x + 1
    yield grid

    while stack:
        pos = stack.pop()
        for Δ in Δs[grid[pos]]:
            if pos + Δ not in cycle:
                cycle.add(pos + Δ)
                stack.append(pos + Δ)
    yield cycle


(H, W), GRID, CYCLE = parse_raw()


def part_one():
    return len(CYCLE) // 2


def part_two():
    ntiles = 0
    for y in range(H):
        inside = False
        for x in range(W):
            pos = complex(x, y)
            if pos not in CYCLE:
                ntiles += inside
            elif GRID[pos] in "|F7":
                inside = not inside
    return ntiles


aoc_lube.submit(year=2023, day=10, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=10, part=2, solution=part_two)
