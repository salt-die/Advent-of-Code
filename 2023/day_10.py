import aoc_lube

N, E, S, W = -1j, 1, 1j, -1
Δs = {"|": (N, S), "J": (N, W), "L": (N, E), "7": (S, W), "F": (S, E), "-": (W, E)}


def parse_raw():
    grid = {}
    for y, line in enumerate(aoc_lube.fetch(year=2023, day=10).splitlines()):
        for x, char in enumerate(line):
            grid[pos := complex(x, y)] = char
            if char == "S":
                grid[pos] = "|"  # by inspection
                stack = [pos]

    yield y + 1, x + 1
    yield grid

    cycle = set()
    while stack:
        cycle.add(pos := stack.pop())
        stack.extend(pos + Δ for Δ in Δs[grid[pos]] if pos + Δ not in cycle)
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
