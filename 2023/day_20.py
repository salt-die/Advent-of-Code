from collections import deque
from itertools import count
from math import lcm, prod

import aoc_lube


def parse_input():
    for line in aoc_lube.fetch(year=2023, day=20).splitlines():
        name, outputs = line.split(" -> ")
        yield name[1:], (name[0], outputs.split(", "))


MODULES = dict(parse_input())


def inputs(module):
    return (in_ for in_, (_, outs) in MODULES.items() if module in outs)


def init_states():
    return {
        module: 0 if type_ == "%" else dict.fromkeys(inputs(module), 0)
        for module, (type_, _) in MODULES.items()
        if type_ != "b"
    }


def part_one():
    states = init_states()
    lohi = [0, 0]
    for _ in range(1000):
        queue = deque([("button", "roadcaster", 0)])

        while queue:
            src, dst, signal = queue.popleft()
            lohi[signal] += 1

            if dst not in MODULES:
                continue

            type_, outs = MODULES[dst]
            if type_ == "%":
                if signal:
                    continue

                states[dst] ^= 1
                output_signal = states[dst]
            elif type_ == "&":
                memory = states[dst]
                memory[src] = signal
                output_signal = not all(memory.values())
            else:
                output_signal = signal

            for out in outs:
                queue.append((dst, out, output_signal))

    return prod(lohi)


def part_two():
    states = init_states()
    sources = set(inputs(*inputs("rx")))
    button_presses = 1

    for i in count(1):
        queue = deque([("button", "roadcaster", 0)])

        while queue:
            src, dst, signal = queue.popleft()
            if src in sources and signal:
                sources.remove(src)
                button_presses = lcm(button_presses, i)
                if not sources:
                    return button_presses

            if dst not in MODULES:
                continue

            type_, outs = MODULES[dst]
            if type_ == "%":
                if signal:
                    continue

                states[dst] ^= 1
                output_signal = states[dst]
            elif type_ == "&":
                memory = states[dst]
                memory[src] = signal
                output_signal = not all(memory.values())
            else:
                output_signal = signal

            for out in outs:
                queue.append((dst, out, output_signal))


aoc_lube.submit(year=2023, day=20, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=20, part=1, solution=part_two)
