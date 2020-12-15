from itertools import product
import re

import aoc_helper

raw = aoc_helper.day(14)

def parse_raw():
    instructions = []
    mask_re = re.compile(r"mask = (.+)")
    mem_re = re.compile(r"mem\[(\d+)\] = (\d+)")
    for line in raw.splitlines():
        if line.startswith("mask"):
            instructions.append(mask_re.match(line).group(1))
        else:
            instructions.append(tuple(map(int, mem_re.match(line).groups((1, 2)))))
    return instructions

data = parse_raw()

def apply_mask(func):
    def wrapper():
        memory = {}
        for instruction in data:
            if isinstance(instruction, str):
                mask = instruction
            else:
                addr, val = instruction
                func(memory, mask, addr, val)
        return sum(memory.values())
    wrapper.__name__ = func.__name__  # aoc_helper expects correct __name__
    return wrapper

@apply_mask
def part_one(memory, mask, addr, val):
    val = bin(val)[2:].zfill(36)
    memory[addr] = int("".join(m if m != "X" else v for m, v in zip(mask, val)), 2)

@apply_mask
def part_two(memory, mask, addr, val):
    addr = bin(addr)[2:].zfill(36)
    masked = "".join(m if m in "1X" else a for m, a in zip(mask, addr)).replace("X", "{}")
    for bin_ in product("01", repeat=mask.count("X")):
        memory[masked.format(*bin_)] = val

aoc_helper.submit(14, part_one)
aoc_helper.submit(14, part_two)
