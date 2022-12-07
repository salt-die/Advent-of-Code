from functools import cached_property
import aoc_lube

RAW = aoc_lube.fetch(year=2022, day=7)


class Path:
    def __init__(self):
        self.directories = {}
        self.files = {}

    @cached_property
    def size(self):
        return (
            sum(self.files.values()) +
            sum(child.size for child in self.directories.values())
        )

    def iter_dir(self):
        yield self

        for child in self.directories.values():
            yield from child.iter_dir()


def parse_raw():
    cwd = system = Path()
    system.directories["/"] = Path()

    for line in RAW.splitlines():
        match line.split():
            case ["$", "cd", ".."]:
                cwd = cwd.parent
            case ["$", "cd", dir_]:
                cwd = cwd.directories[dir_]
            case ["$", "ls"]:
                pass
            case ["dir", dir_]:
                if dir_ not in cwd.directories:
                    node = Path()
                    cwd.directories[dir_] = node
                    node.parent = cwd
            case [size, file]:
                cwd.files[file] = int(size)

    return system

SYSTEM = parse_raw()

def part_one():
    return sum(
        size
        for dir in SYSTEM.iter_dir()
        if (size := dir.size) <= 100000
    )

def part_two():
    needed = SYSTEM.size - 40_000_000

    return min(
        dir_.size
        for dir_ in SYSTEM.iter_dir()
        if dir_.size > needed
    )

aoc_lube.submit(year=2022, day=7, part=1, solution=part_one)
aoc_lube.submit(year=2022, day=7, part=2, solution=part_two)
