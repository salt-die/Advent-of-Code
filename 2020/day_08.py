import aoc_helper
import intcode as ic

raw = aoc_helper.day(8)

def parse_raw():
    out = []
    for line in raw.splitlines():
        out.append((line.split()[0], int(line.split()[1])))
    return out

boot_program = ic.Computer(parse_raw())

def part_one():
    try:
        boot_program.run()
    except ic.CycleError as e:
        return e.args[0]

def part_two():
    return boot_program.fsck()

aoc_helper.submit(8, part_one)
aoc_helper.submit(8, part_two)
