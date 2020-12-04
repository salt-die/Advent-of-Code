import aoc_helper
from utils import adict
import re

raw = aoc_helper.day(4)

FIELDS = "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"

def parse_raw():
    passports = []
    passport = {}
    for line in raw.splitlines():
        if not line:
            passports.append(adict(passport))
            passport = {}
        else:
            passport.update({field: match.group(1) for field in FIELDS if (match := re.search(rf"{field}:(\S+)", line))})
    return passports

data = parse_raw()

def part_one():
    return sum(len(passport) == len(FIELDS) for passport in data)

def part_two():
    HCL_RE = re.compile(r"^#[0-9a-f]{6}$")
    PID_RE = re.compile(r"^\d{9}$")

    return sum(     len(passport) == len(FIELDS)
               and  1920 <= int(passport.byr) <= 2002
               and  2010 <= int(passport.iyr) <= 2020
               and  2020 <= int(passport.eyr) <= 2030
               and  (   passport.hgt.endswith("cm") and 150 <= int(passport.hgt[:-2]) <= 193
                     or passport.hgt.endswith("in") and  59 <= int(passport.hgt[:-2]) <= 76)
               and bool(HCL_RE.match(passport.hcl))
               and passport.ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
               and bool(PID_RE.match(passport.pid))
                for passport in data)

aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)
