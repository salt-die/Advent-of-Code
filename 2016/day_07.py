import aoc_lube
from aoc_lube.utils import sliding_window, distribute

def parse_data():
    for line in aoc_lube.fetch(year=2016, day=7).splitlines():
        a, b = distribute(line.replace("[", " ").replace("]", " ").split(), 2)
        yield list(a), list(b)

IPS = list(parse_data())

def contains_abba(it):
    return any(a == d != b == c for a, b, c, d in sliding_window(it, 4))

def supports_tls(ip):
    supernets, hypernets = ip
    return not any(map(contains_abba, hypernets)) and any(map(contains_abba, supernets))

def supports_ssl(ip):
    supernets, hypernets = ip
    return any(
        a == c != b and any(f"{b}{a}{b}" in hypernet for hypernet in hypernets)
        for supernet in supernets
        for a, b, c in sliding_window(supernet, 3)
    )

def part_one():
    return sum(map(supports_tls, IPS))

def part_two():
    return sum(map(supports_ssl, IPS))

aoc_lube.submit(year=2016, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2016, day=7, part=2, solution=part_two)
