import aoc_lube

RAW = aoc_lube.fetch(year=2016, day=1)
DATA = [(1j if instruction[0] == "L" else -1j, int(instruction[1:])) for instruction in RAW.split(", ")]

def traverse():
    direction = 1j
    location = 0j
    yield location
    for turn, steps in DATA:
        direction *= turn
        for _ in range(steps):
            location += direction
            yield location

def manhattan(pos: complex) -> int:
    return abs(int(pos.real)) + abs(int(pos.imag))

def part_one():
    for location in traverse():
        pass
    return manhattan(location)

def part_two():
    visited = set()
    for location in traverse():
        if location in visited:
            return manhattan(location)
        visited.add(location)

aoc_lube.submit(year=2016, day=1, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=1, part=2, solution=part_two)
