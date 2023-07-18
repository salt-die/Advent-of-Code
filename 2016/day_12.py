import aoc_lube

INSTRUCTIONS = [
    [int(s) if s.isdigit() or s.startswith("-") else s for s in line.split()]
    for line in aoc_lube.fetch(year=2016, day=12).splitlines()
]

def execute(registers):
    addr = 0
    while addr < len(INSTRUCTIONS):
        match INSTRUCTIONS[addr]:
            case "inc", reg:
                registers[reg] += 1
            case "dec", reg:
                registers[reg] -= 1
            case "cpy", val, reg:
                registers[reg] = registers.get(val, val)
            case "jnz", val, jmp if registers.get(val, val):
                addr += int(jmp)
                continue
        addr += 1
    return registers["a"]

def part_one():
    return execute(dict(a=0, b=0, c=0, d=0))

def part_two():
    return execute(dict(a=0, b=0, c=1, d=0))

aoc_lube.submit(year=2016, day=12, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=12, part=2, solution=part_two)
