import aoc_lube
from aoc_lube.utils import chinese_remainder_theorem, chunk, extract_ints

DISCS = [(b, d) for _, b, _, d in chunk(extract_ints(aoc_lube.fetch(year=2016, day=15)), 4)]

def solve_discs():
    moduli = [a for a, _ in DISCS]
    residues = [-b - i for i, (_, b) in enumerate(DISCS, start=1)]
    return chinese_remainder_theorem(moduli, residues)

aoc_lube.submit(year=2016, day=15, part=1, solution=solve_discs)

DISCS.append((11, 0))
aoc_lube.submit(year=2016, day=15, part=2, solution=solve_discs)
