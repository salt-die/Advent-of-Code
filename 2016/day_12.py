import aoc_lube

INSTRUCTIONS = aoc_lube.fetch(year=2016, day=12).splitlines()

def execute(registers):
    addr = 0
    while addr < len(INSTRUCTIONS):
        match INSTRUCTIONS[addr].split():
            case "inc", reg:
                registers[reg] += 1
            case "dec", reg:
                registers[reg] -= 1
            case "cpy", val, reg:
                registers[reg] = int(val) if val.isdigit() else registers[val]
            case "jnz", val, jmp if val.isdigit() and val != "0" or registers[val] != 0:
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
