import aoc_helper

RAW = aoc_helper.day(6)

NSTATES = 9
FISH = [0] * NSTATES

for n in aoc_helper.utils.extract_ints(RAW):
    FISH[n] += 1

def nfish(days):
    all_fish = FISH.copy()

    for i in range(days):
        all_fish[(i + 7) % NSTATES] += all_fish[i % NSTATES]

    return sum(all_fish)

def part_one():
    return nfish(80)

def part_two():
    return nfish(256)

aoc_helper.submit(6, part_one)
aoc_helper.submit(6, part_two)
