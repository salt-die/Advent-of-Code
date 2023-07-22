import aoc_lube
from aoc_lube.utils import chunk

def fill_disk(fill_length):
    state = aoc_lube.fetch(year=2016, day=16)
    invert = str.maketrans("01", "10")

    while len(state) < fill_length:
        state = f"{state}0{state[::-1].translate(invert)}"

    state = state[:fill_length]

    while len(state) % 2 == 0:
        state = "".join("01"[a == b] for a, b in chunk(state, 2))

    return state

aoc_lube.submit(year=2016, day=16, part=1, solution=lambda: fill_disk(272))
aoc_lube.submit(year=2016, day=16, part=2, solution=lambda: fill_disk(35651584))
