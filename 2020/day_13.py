import aoc_helper
from sympy.ntheory.modular import crt

raw = aoc_helper.day(13)

def parse_raw():
    departure_time, ids = raw.splitlines()
    moduli = []
    residues = []
    for residue, modulus in enumerate(ids.split(",")):
        if modulus.isdigit():
            moduli.append(int(modulus))
            residues.append(-residue)
    return int(departure_time), moduli, residues

departure, moduli, residues = parse_raw()

def part_one():
    bus_id = min(moduli, key=lambda bus_id: -departure % bus_id)
    return (-departure % bus_id) * bus_id

def part_two():
    return crt(moduli, residues)[0]  # Chinese remainder theorem

aoc_helper.submit(13, part_one)
aoc_helper.submit(13, part_two)
