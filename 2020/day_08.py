import re

import aoc_helper
import intcode as ic

raw = aoc_helper.day(8)
data = [(op, int(val)) for op, val in re.findall(r"(.+) (.+)", raw)]
boot_program = ic.Computer(data)

def part_one():
    try:
        boot_program.run()
    except ic.CycleError as e:
        return e.args[0]

def part_two():
    return boot_program.fsck()

aoc_helper.submit(8, part_one)
aoc_helper.submit(8, part_two)
