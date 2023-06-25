import aoc_lube

NUMBERS = aoc_lube.fetch(year=2016, day=2).split()
DIRS = dict(U=(-1, 0), D=(1, 0), L=(0, -1), R=(0, 1))

def get_password(keypad, start, validate):
    password = ""
    for number in NUMBERS:
        y, x = start
        for instruction in number:
            dy, dx = DIRS[instruction]
            if validate(y + dy, x + dx):
                y += dy
                x += dx
        password += keypad[y][x]
    return password

def part_one():
    return get_password(
        keypad=["123", "456", "789"],
        start=(1, 1),
        validate=lambda y, x: max(abs(y - 1), abs(x - 1)) <= 1,
    )

def part_two():
    return get_password(
        keypad=["--1--", "-234-", "56789", "-ABC-", "--D--"],
        start=(2, 0),
        validate=lambda y, x: abs(y - 2) + abs(x - 2) <= 2,
    )

aoc_lube.submit(year=2016, day=2, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=2, part=2, solution=part_two)
