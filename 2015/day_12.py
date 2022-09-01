import json

import aoc_helper
from aoc_helper.utils import extract_ints

def part_one():
    return sum(extract_ints(aoc_helper.day(12)))

def count(account):
    match account:
        case dict():
            if "red" in account.values():
                return 0
            return sum(map(count, account.values()))
        case list():
            return sum(map(count, account))
        case str():
            return 0
        case int():
            return account

def part_two():
    account = json.loads(aoc_helper.day(12))
    return count(account)

aoc_helper.submit(12, part_one)
aoc_helper.submit(12, part_two)
