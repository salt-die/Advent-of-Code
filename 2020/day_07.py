import aoc_helper
import re

raw = aoc_helper.day(7)

def parse_raw():
    bags = re.findall(r"([a-z]+ [a-z]+) bags contain (.+)", raw)
    formula = re.compile(r"(\d+) ([a-z]+ [a-z]+) bag")
    return {bag: {inner: int(n) for n, inner in formula.findall(contents)} for bag, contents in bags}

formulas = parse_raw()

def has_shiny(bag):
    return "shiny gold" in formulas[bag] or any(map(has_shiny, formulas[bag]))

def count(bag):
    return 1 + sum(n * count(inner) for inner, n in formulas[bag].items())

def part_one():
    return sum(map(has_shiny, formulas))

def part_two():
    return count("shiny gold") - 1  # -1 since we don't count the shiny gold bag itself!

aoc_helper.submit(7, part_one)
aoc_helper.submit(7, part_two)

# Alternative part 1, stack-based:
# def has_shiny(bag):
#     stack = [bag]
#     while stack:
#         current = stack.pop()
#         if "shiny gold" in formulas[current]:
#             return True
#         stack.extend(formulas[current])
#     return False
#
# Alternatives part 2: Both stack-based, one builds an arithmetic expression, the other consumes output as soon as it can
# def count(bag):
#     tokens = deque(formulas[bag].items())
#     stack = []
#     while tokens:
#         current, amt = tokens.popleft()
#         stack.extend(f"+{amt}")
#         if formulas[current]:
#             stack.extend("*(1+")
#             tokens.appendleft(")")
#             tokens.extendleft(formulas[current].items())
#             continue
#
#         while tokens and tokens[0] == ")":
#             stack.append(tokens.popleft())
#
#     return eval("".join(stack))
#
# def count(bag):
#     tokens = list(formulas[bag].items())
#     output = []
#     while tokens:
#         current, amt = tokens.pop()
#         output.append(amt)
#         if formulas[current]:
#             output.append(1)
#             tokens.append(")")
#             tokens.extend(formulas[current].items())
#             continue
#
#         while tokens:
#             if tokens[-1] == ")":
#                 output.append((output.pop() + output.pop()) * output.pop())
#                 tokens.pop()
#             else:
#                 if len(output) > 1:
#                     output.append(output.pop() + output.pop())
#                 break
#
#     return sum(output)