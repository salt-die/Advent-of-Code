from math import prod

import aoc_lube


def parse_raw():
    workflows, parts = aoc_lube.fetch(year=2023, day=19).split("\n\n")
    workflow_dict = {}
    for line in workflows.splitlines():
        name, instructions = line[:-1].split("{")
        *normal, last = instructions.split(",")
        commands = []
        for cmd in normal:
            cnd, goto = cmd.split(":")
            op = ">" if ">" in cnd else "<"
            cat, n = cnd.split(op)
            commands.append((cat, op, int(n), goto))
        commands.append(last)
        workflow_dict[name] = commands

    part_tuples = []
    for part in parts.splitlines():
        part_tuples.append(eval(f"dict({part[1:-1]})"))
    return workflow_dict, part_tuples


WORKFLOWS, PARTS = parse_raw()


def part_one():
    total = 0
    for part in PARTS:
        workflow = "in"
        while workflow not in "RA":
            for cmd in WORKFLOWS[workflow]:
                if isinstance(cmd, str):
                    workflow = cmd
                else:
                    cat, op, n, goto = cmd
                    m = part[cat]
                    if op == ">" and m > n or op == "<" and m < n:
                        workflow = goto
                        break

        if workflow == "A":
            total += sum(part.values())
    return total


def nvalid(workflow, part):
    if workflow == "R":
        yield 0
        return

    if workflow == "A":
        yield prod(hi - lo + 1 for lo, hi in part.values())
        return

    for cmd in WORKFLOWS[workflow]:
        if isinstance(cmd, str):
            yield from nvalid(cmd, part)
        else:
            cat, op, n, goto = cmd
            lo, hi = part[cat]

            if op == "<":
                if lo < n:
                    yield from nvalid(goto, part | {cat: (lo, n - 1)})

                if hi < n:
                    break

                part = part | {cat: (n, hi)}
            else:
                if n < hi:
                    yield from nvalid(goto, part | {cat: (n + 1, hi)})

                if n < lo:
                    break
                part = part | {cat: (lo, n)}


def part_two():
    return sum(nvalid("in", dict(zip("xmas", ((1, 4000),) * 4))))


aoc_lube.submit(year=2023, day=19, part=1, solution=part_one)
aoc_lube.submit(year=2023, day=19, part=2, solution=part_two)
