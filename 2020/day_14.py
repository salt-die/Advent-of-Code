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
    memory = {}
    for instruction in data:
        if isinstance(instruction, str):  # mask
            mask = instruction
        else:
            addr, val = instruction
            func(memory, mask, addr, val)
    return sum(memory.values())

@apply_mask
def masked_v1(memory, mask, addr, val):
    val = bin(val)[2:].zfill(36)
    memory[addr] = int("".join(m if m != "X" else b for m, b in zip(mask, val)), 2)

@apply_mask
def masked_v2(memory, mask, addr, val):
    addr = bin(addr)[2:].zfill(36)
    masked = "".join(m if m in "1X" else a for m, a in zip(mask, addr)).replace("X", "{}")
    for wer in product("01", repeat=mask.count("X")):
        memory[masked.format(*wer)] = val

def part_one():
    return masked_v1

def part_two():
    return masked_v2

aoc_helper.submit(14, part_one)
aoc_helper.submit(14, part_two)
