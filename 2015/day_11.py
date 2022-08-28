import aoc_helper

def get_next_valid(password):
    # This isn't a general solution: Since we only need to generate two valid passwords,
    # we assume no invalid characters at the start of the string, and no doubles or ascending
    # characters in the initial password (which is true for our puzzle input, by inspection).
    as_int = list(map(ord, password))
    if as_int[3] <= as_int[4]:
        as_int[3] += 1

    if (i := as_int[3]) <= ord("x"):
        as_int[3:] = i, i, i + 1, i + 2, i + 2
    else:
        as_int[2] += 1
        as_int[3:] = map(ord, "aabcc")

    return "".join(map(chr, as_int))

def part_one():
    return get_next_valid(aoc_helper.day(11))

def part_two():
    return get_next_valid(part_one())

aoc_helper.submit(11, part_one)
aoc_helper.submit(11, part_two)
