import aoc_lube
from aoc_lube.utils import extract_ints, chunk, chinese_remainder_theorem

RAW = aoc_lube.fetch(year=2016, day=15)
DISCS = [(b, d) for _, b, _, d in chunk(extract_ints(RAW), 4)]

def solve_discs():
    moduli = [a for a, _ in DISCS]
    residues = [a - b - i for i, (a, b) in enumerate(DISCS, start=1)]
    return chinese_remainder_theorem(moduli, residues)

def part_one():
    return solve_discs()

def part_two():
    DISCS.append((11, 0))
    return solve_discs()

aoc_lube.submit(year=2016, day=15, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=15, part=2, solution=part_two)
