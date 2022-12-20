from math import prod

import aoc_lube
from aoc_lube.utils import extract_ints, chunk
from cpmpy import Model, cpm_array, intvar, boolvar

BLUEPRINTS = list(chunk(extract_ints(aoc_lube.fetch(year=2022, day=19)), 7))

def solve(blueprints, duration):
    duration += 1

    for _, a, b, c, d, e, f in blueprints:
        costs = cpm_array([[a, 0, 0, 0], [b, 0, 0, 0], [c, d, 0, 0], [e, 0, f, 0]])
        bot_to_build = boolvar(shape=(duration, 4))
        nbots = intvar(0, duration, shape=(duration, 4))
        resources = intvar(0, duration**2, shape=(duration, 4))

        model = Model(
            resources[0] == 0,
            nbots[0] == [1, 0, 0, 0],
            resources >= bot_to_build @ costs,
            resources[1:] == resources[:-1] - bot_to_build[:-1] @ costs + nbots[:-1],
            nbots[1:] == nbots[:-1] + bot_to_build[:-1],
            [row.sum() <= 1 for row in bot_to_build],
        )

        model.maximize(resources[-1][-1])
        model.solve()
        yield resources[-1][-1].value()

def part_one():
    return sum(i * ngeodes for i, ngeodes in enumerate(solve(BLUEPRINTS, 24), start=1))

def part_two():
    return prod(solve(BLUEPRINTS[:3], 32))

aoc_lube.submit(year=2022, day=19, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=19, part=2, solution=part_two)
