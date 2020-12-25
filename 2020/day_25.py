import aoc_helper

raw = aoc_helper.day(25)
card_key, door_key = aoc_helper.extract_ints(raw)
MOD = 20201227

def part_one():
    for n in range(1, MOD):
        if  (s := pow(7, n, MOD)) == card_key:
            return pow(door_key, n, MOD)
        elif s == door_key:
            return pow(card_key, n, MOD)

aoc_helper.submit(25, part_one)
