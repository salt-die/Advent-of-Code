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

# Alternative Iterative solution:
# def has_shiny(bag):
#     stack = [bag]
#     while stack:
#         current = stack.pop()
#         if "shiny gold" in formulas[current]:
#             return True
#         stack.extend(formulas[current])
#     return False

def count(bag):
    return 1 + sum(n * count(inner) for inner, n in formulas[bag].items())


#  How about another stack solution, but one that builds an very long arithmetic expression to eval?!
# from collections import deque
#
# def count(bag):
#     tokens = deque(formulas[bag].items())
#     stack = []
#     while tokens:
#         current, amt = tokens.popleft()
#         stack.append(str(amt))
#         if formulas[current]:
#             stack.extend("*(")
#             tokens.appendleft(")")
#             tokens.extendleft(formulas[current].items())
#             continue

#         while tokens:
#             if tokens[0] == ")":
#                 stack.extend("+1")
#                 stack.append(tokens.popleft())
#             else:
#                 stack.append("+")
#                 break
#     return eval("".join(stack))

def part_one():
    return sum(map(has_shiny, formulas))

def part_two():
    return count("shiny gold") - 1  # -1 since we don't count the shiny gold bag itself!
print(part_two())
aoc_helper.submit(7, part_one)
aoc_helper.submit(7, part_two)
