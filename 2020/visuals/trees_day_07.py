import re

def prefix(first, rest, lines):
    it = iter(lines.splitlines())
    yield first + next(it)
    for line in it:
        yield rest + line

class Bag:
    def __init__(self, name, bags):
        self.name = f"{name} bag"
        self.bags = bags

    def __str__(self):
        if not self.bags:
            return self.name

        *body, last = self.bags.items()
        return '\n'.join(
            (
                self.name,
                *(line for bag, n in body for line in prefix(' ├─', ' │ ', f"{n} {bag}")),
                *prefix(" ╰─", "   ", f"{last[1]} {last[0]}"),
            )
        )

with open("day_07_input.txt") as f:
    raw = f.read()

def parse_raw():
    bag_description = r"([a-z]+ [a-z]+) bags contain (.+)"
    formula = re.compile(r"(\d+) ([a-z]+ [a-z]+) bag")
    bags = {bag: Bag(bag, contents) for bag, contents in re.findall(bag_description, raw)}
    for bag in bags.values():
        bag.bags = {bags[inner]: n for n, inner in formula.findall(bag.bags)}
    return bags

bags = parse_raw()

def pp(bag):
    print(bags[bag])
