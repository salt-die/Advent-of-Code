import re
from functools import reduce
from itertools import product
from math import prod

import aoc_helper
from more_itertools import partition
from real_ranges import RangeSet, Var

raw = aoc_helper.day(16)
x = Var('x')

def parse_raw():
    rules, my_ticket, nearby_tickets = raw.split("\n\n")

    rules_pattern = re.compile(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)")
    fields = {}
    for line in rules.splitlines():
        field, start_1, end_1, start_2, end_2 = rules_pattern.match(line).groups()
        fields[field] = (int(start_1) <= x <= int(end_1)) | (int(start_2) <= x <= int(end_2))

    my_ticket = list(aoc_helper.extract_ints(my_ticket))
    nearby_tickets = [list(aoc_helper.extract_ints(line)) for line in nearby_tickets.splitlines()[1:]]

    return fields, my_ticket, nearby_tickets

fields, my_ticket, nearby_tickets = parse_raw()

valid_values = reduce(RangeSet.__or__, fields.values())

def is_valid(ticket):
    return all(i in valid_values for i in ticket)

invalid_tickets, valid_tickets = map(list, partition(is_valid, nearby_tickets))

def part_one():
    return sum(i for ticket in invalid_tickets for i in ticket if i not in valid_values)

def part_two():
    # Create a list of (field, set of possible indices for field) pairs, sorted by length of set
    possible_indices = [(field, set()) for field in fields]
    for (field, indices), i in product(possible_indices, range(len(fields))):
        if all(ticket[i] in fields[field] for ticket in valid_tickets):
            indices.add(i)
    possible_indices.sort(key=lambda tup: len(tup[1]), reverse=True)

    # Process of elimination to match fields to their index
    index_to_field = [None] * len(fields)
    for _ in fields:
        field, (i,) = possible_indices.pop()
        index_to_field[i] = field
        for _, indices in possible_indices:
            indices.remove(i)

    return prod(my_ticket[i] for i, field in enumerate(index_to_field) if field.startswith("departure"))

aoc_helper.submit(16, part_one)
aoc_helper.submit(16, part_two)
