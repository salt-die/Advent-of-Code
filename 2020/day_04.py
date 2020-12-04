import aoc_helper
import re

FIELDS = "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"

raw = aoc_helper.day(4)
passports = [dict(matches) for line in raw.split("\n\n") if len(matches := re.findall(r"(?!cid)([a-z]{3}):(\S+)", line)) == len(FIELDS)]

def part_one():
    return len(passports)

def part_two():
    RES = (
        r"19[2-9][\d]|200[0-2]",                       # byr
        r"201[\d]|2020",                               # iyr
        r"202[\d]|2030",                               # eyr
        r"1([5-8][\d]|9[0-3])cm|(59|6[\d]|7[0-6])in",  # hgt
        r"#[0-9a-f]{6}",                               # hcl
        r"amb|blu|brn|gr(y|n)|hzl|oth",                # ecl
        r"\d{9}",                                      # pid
    )
    return sum(all(map(bool, map(re.fullmatch, RES, map(pp.__getitem__, FIELDS)))) for pp in passports)

print(part_one(), part_two())
aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)