import aoc_helper

RAW = aoc_helper.day(8)

DATA = [
    [patterns.split() for patterns in line.split("|")]
    for line in RAW.splitlines()
]

def part_one():
    return sum(
        sum(len(digit) in {2, 3, 4, 7} for digit in output_digits)
        for _, output_digits in DATA
    )

DECODE = {
    (6, 2, 3): 0,
    (2, 2, 2): 1,
    (5, 1, 2): 2,
    (5, 2, 3): 3,
    (4, 2, 4): 4,
    (5, 1, 3): 5,
    (6, 1, 3): 6,
    (3, 2, 2): 7,
    (7, 2, 4): 8,
    (6, 2, 4): 9,
}

def decode(data):
    signal_patterns, output_digits = data

    one = four = None
    for pattern in signal_patterns:
        if len(pattern) == 2:
            one = set(pattern)
        elif len(pattern) == 4:
            four = set(pattern)

        if one and four:
            break

    return sum(
        10**(3 - i) * DECODE[
            len(digit),
            len(one.intersection(digit)),
            len(four.intersection(digit)),
        ]
        for i, digit in enumerate(output_digits)
    )

def part_two():
    return sum(map(decode, DATA))

aoc_helper.submit(8, part_one)
aoc_helper.submit(8, part_two)
