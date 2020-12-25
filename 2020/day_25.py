import aoc_helper

raw = aoc_helper.day(25)
card_key, door_key = aoc_helper.extract_ints(raw)

def part_one():
    for n in range(1, 20201227):
        s = pow(7, n, 20201227)

        if  s == card_key:
            return pow(door_key, n, 20201227)
        elif s == door_key:
            return pow(card_key, n, 20201227)

aoc_helper.submit(25, part_one)
