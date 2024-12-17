from heapq import heappop, heappush

import aoc_lube
from aoc_lube.utils import extract_ints

HP, DAMAGE = extract_ints(aoc_lube.fetch(year=2015, day=22))


def simulate_fight(part=1):
    heap = [(0, 500, 50, HP, 0, 0, 0, 0)]
    while heap:
        spent, mana, health, boss_health, shield, poison, recharge, turn = heappop(heap)

        if part == 2 and turn:
            health -= 1
            if health <= 0:
                continue
        if shield:
            shield -= 1
            boss_damage = max(DAMAGE - 7, 1)
        else:
            boss_damage = DAMAGE
        if poison:
            poison -= 1
            boss_health -= 3
        if recharge:
            recharge -= 1
            mana += 101
        if boss_health <= 0:
            return spent

        # fmt: off
        if turn:
            health -= boss_damage
            if health > 0:
                heappush(heap, (spent, mana, health, boss_health, shield, poison, recharge, 0))
        else:
            if mana >= 53:
                heappush(heap, (spent + 53, mana - 53, health, boss_health - 4, shield, poison, recharge, 1))
            if mana >= 73:
                heappush(heap, (spent + 73, mana - 73, health + 2, boss_health - 2, shield, poison, recharge, 1))
            if mana >= 113 and not shield:
                heappush(heap, (spent + 113, mana - 113, health, boss_health, 6, poison, recharge, 1))
            if mana >= 173 and not poison:
                heappush(heap, (spent + 173, mana - 173, health, boss_health, shield, 6, recharge, 1))
            if mana >= 229 and not recharge:
                heappush(heap, (spent + 229, mana - 229, health, boss_health, shield, poison, 5, 1))
        # fmt: on


def part_one():
    return simulate_fight()


def part_two():
    return simulate_fight(2)


aoc_lube.submit(year=2015, day=22, part=1, solution=part_one)
aoc_lube.submit(year=2015, day=22, part=2, solution=part_two)
