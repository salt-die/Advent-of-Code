import aoc_helper
from lark import Lark, LarkError

raw = aoc_helper.day(19)
rules, messages = raw.split("\n\n")

def valid_messages(rules):
    grammar = rules.translate(str.maketrans("0123456789", "abcdefghij"))  # Rule names can't be numeric
    parser = Lark(grammar, start="a")
    valid = 0
    for message in messages.splitlines():
        try:
            parser.parse(message)
        except LarkError:
            pass
        else:
            valid += 1
    return valid

def part_one():
    return valid_messages(rules)

def part_two():
    new_rules = rules.replace('8: 42', '8: 42 | 42 8').replace('11: 42 31', '11: 42 31 | 42 11 31')
    return valid_messages(new_rules)

aoc_helper.submit(19, part_one)
aoc_helper.submit(19, part_two)
