import aoc_helper
from utils import adict
import re

raw = aoc_helper.day(4)
passports = [adict(re.findall(r"(?!cid)([a-z]{3}):(\S+)", line)) for line in raw.split("\n\n")]

def part_one():
    return sum(len(pp) == 7 for pp in passports)

def part_two():
    HCL_RE = re.compile(r"^#[0-9a-f]{6}$")
    PID_RE = re.compile(r"^\d{9}$")

    return sum(     len(pp) == 7
               and  1920 <= int(pp.byr) <= 2002
               and  2010 <= int(pp.iyr) <= 2020
               and  2020 <= int(pp.eyr) <= 2030
               and  (   pp.hgt.endswith("cm") and 150 <= int(pp.hgt[:-2]) <= 193
                     or pp.hgt.endswith("in") and  59 <= int(pp.hgt[:-2]) <= 76)
               and bool(HCL_RE.match(pp.hcl))
               and pp.ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
               and bool(PID_RE.match(pp.pid))
                for pp in passports)

aoc_helper.submit(4, part_one)
aoc_helper.submit(4, part_two)
