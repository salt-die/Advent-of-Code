from typing import NamedTuple

import aoc_helper
from aoc_helper.utils import extract_ints


class Interval(NamedTuple):
    start: int
    stop: int

    @property
    def length(self):
        return max(0, self.stop - self.start + 1)

    def __bool__(self):
        return self.length > 0

    def intersects(self, other):
        return self.start <= other.stop and self.stop >= other.start

    def intersection(self, other):
        return Interval(max(self.start, other.start), min(self.stop, other.stop))

    def clip(self, mi, mx):
        start, stop = self
        return Interval(max(mi, start), min(mx, stop))


class Cuboid(NamedTuple):
    height: Interval
    width: Interval
    depth: Interval

    @property
    def volume(self):
        return self.height.length * self.width.length * self.depth.length

    def intersects(self, other):
        return (
            self.height.intersects(other.height)
            and self.width.intersects(other.width)
            and self.depth.intersects(other.depth)
        )

    def intersection(self, other):
        return Cuboid(
            *(i.intersection(j) for i, j in zip(self, other))
        )

    def clip(self, mi, mx):
        h, w, d = self
        return Cuboid(h.clip(mi, mx), w.clip(mi, mx), d.clip(mi, mx))


def difference(a: Cuboid, b: Cuboid):
    if not a.intersects(b):
        yield a
        return

    overlap = a.intersection(b)

    if i := Interval(a.depth.start, overlap.depth.start - 1):
        yield Cuboid(a.height, a.width, i)

    if i := Interval(overlap.depth.stop + 1, a.depth.stop):
        yield Cuboid(a.height, a.width, i)

    if i := Interval(a.height.start, overlap.height.start - 1):
        yield Cuboid(i, a.width, overlap.depth)

    if i := Interval(overlap.height.stop + 1, a.height.stop):
        yield Cuboid(i, a.width, overlap.depth)

    if i := Interval(a.width.start, overlap.width.start - 1):
        yield Cuboid(overlap.height, i, overlap.depth)

    if i := Interval(overlap.width.stop + 1, a.width.stop):
        yield Cuboid(overlap.height, i, overlap.depth)

def parse_raw():
    for line in aoc_helper.day(22).splitlines():
        it = extract_ints(line)
        yield line.startswith("on"), Cuboid(*map(Interval, it, it))

def regionify():
    """
    Split intersecting cubes into individual regions.
    """
    nonintersecting = [ ]
    for is_on, current in parse_raw():
        differences = [ ]
        for cuboid in nonintersecting:
            differences.extend(difference(cuboid, current))

        if is_on:
            differences.append(current)

        nonintersecting = differences

    return nonintersecting

CUBOIDS = regionify()

def part_one():
    return sum(cuboid.clip(-50, 50).volume for cuboid in CUBOIDS)

def part_two():
    return sum(cuboid.volume for cuboid in CUBOIDS)

aoc_helper.submit(22, part_one)
aoc_helper.submit(22, part_two)
