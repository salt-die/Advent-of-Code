import aoc_lube

INSTRUCTIONS = aoc_lube.fetch(year=2015, day=23).splitlines()
print(INSTRUCTIONS)


def compute(a):
    registers = {"a": a, "b": 0}
    ptr = 0
    while ptr < len(INSTRUCTIONS):
        match INSTRUCTIONS[ptr].split():
            case "hlf", register:
                registers[register] //= 2
            case "tpl", register:
                registers[register] *= 3
            case "inc", register:
                registers[register] += 1
            case "jmp", amount:
                ptr += int(amount) - 1
            case "jie", register, amount:
                if registers[register[0]] % 2 == 0:
                    ptr += int(amount) - 1
            case "jio", register, amount:
                if registers[register[0]] == 1:
                    ptr += int(amount) - 1
        ptr += 1
    return registers["b"]


def part_one():
    return compute(0)


def part_two():
    return compute(1)


aoc_lube.submit(year=2015, day=23, part=1, solution=part_one)
aoc_lube.submit(year=2015, day=23, part=2, solution=part_two)
