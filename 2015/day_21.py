from dataclasses import dataclass
from itertools import product

import aoc_lube
from aoc_lube.utils import extract_ints


@dataclass
class Mob:
    hit_points: int
    damage: int
    armor: int


BOSS_STATS = tuple(extract_ints(aoc_lube.fetch(year=2015, day=21)))
WEAPONS = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
ARMOR = [(13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5), (0, 0, 0)]
RINGS = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
    (0, 0, 0),
    (0, 0, 0),
]


def simulate_fight(*equipment):
    player = Mob(100, 0, 0)
    boss = Mob(*BOSS_STATS)
    for _, damage, armor in equipment:
        player.damage += damage
        player.armor += armor

    while True:
        boss.hit_points -= max(player.damage - boss.armor, 1)
        if boss.hit_points <= 0:
            return True
        player.hit_points -= max(boss.damage - player.armor, 1)
        if player.hit_points <= 0:
            return False


def cost(*equipment):
    return sum(cost for cost, *_ in equipment)


def part_one():
    return min(
        cost(weapon, armor, ring1, ring2)
        for weapon, armor, ring1, ring2 in product(WEAPONS, ARMOR, RINGS, RINGS)
        if ring1 is not ring2 and simulate_fight(weapon, armor, ring1, ring2)
    )


def part_two():
    return max(
        cost(weapon, armor, ring1, ring2)
        for weapon, armor, ring1, ring2 in product(WEAPONS, ARMOR, RINGS, RINGS)
        if ring1 is not ring2 and not simulate_fight(weapon, armor, ring1, ring2)
    )


aoc_lube.submit(year=2015, day=21, part=1, solution=part_one)
aoc_lube.submit(year=2015, day=21, part=2, solution=part_two)
