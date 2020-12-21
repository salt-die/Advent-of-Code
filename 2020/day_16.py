import re
from functools import reduce
from math import prod

import aoc_helper
from more_itertools import partition
import networkx as nx
from real_ranges import Range, RangeSet # https://github.com/salt-die/real_ranges

raw = aoc_helper.day(16)

def parse_raw():
    rules, my_ticket, nearby_tickets = raw.split("\n\n")

    fields = {
        field: Range(f"[{p}, {q}]") | Range(f"[{r}, {s}]")
        for field, p, q, r, s in re.findall(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", rules)
    }
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

def valid_indices(field):
    """Return all possible indices for `field`."""
    return set(i for i in range(len(fields)) if all(ticket[i] in fields[field] for ticket in valid_tickets))

def part_two():
    possible_indices = {field: valid_indices(field) for field in fields}
    G = nx.from_dict_of_lists(possible_indices)
    return prod(my_ticket[i] for i, field in nx.bipartite.maximum_matching(G).items() if field in fields and field.startswith("departure"))

aoc_helper.submit(16, part_one)
aoc_helper.submit(16, part_two)
