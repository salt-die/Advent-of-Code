import aoc_lube

INIT_SEQUENCE = aoc_lube.fetch(year=2023, day=15).split(",")


def hash(string):
    total = 0
    for char in string:
        total += ord(char)
        total *= 17
    return total % 256


def part_one():
    return sum(map(hash, INIT_SEQUENCE))


def part_two():
    boxes = [{} for _ in range(256)]
    for s in INIT_SEQUENCE:
        if s.endswith("-"):
            box = s[:-1]
            boxes[hash(box)].pop(box, None)
        else:
            box, n = s.split("=")
            boxes[hash(box)][box] = int(n)
    return sum(
        i * j * focal
        for i, box in enumerate(boxes, start=1)
        for j, focal in enumerate(box.values(), start=1)
    )


aoc_lube.submit(year=2023, day=15, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=15, part=2, solution=part_two)
