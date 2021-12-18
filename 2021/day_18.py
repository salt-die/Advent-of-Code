from ast import literal_eval
from functools import reduce
from itertools import product
from math import ceil, floor

import aoc_helper

def isnode(node):
    return isinstance(node, BinaryNode)


class BinaryNode:
    def __init__(self, left, right, parent=None):
        self.left = left
        if isnode(left):
            left.parent = self

        self.right = right
        if isnode(right):
            right.parent = self

        self.parent = parent

    def iter_nodes(self):
        if isnode(self.left):
            yield from self.left.iter_nodes()

        yield self

        if isnode(self.right):
            yield from self.right.iter_nodes()

    @property
    def leftmost(self):
        return self.left.leftmost if isnode(self.left) else self

    @property
    def rightmost(self):
        return self.right.rightmost if isnode(self.right) else self

    @property
    def is_root(self):
        return self.parent is None

    @property
    def previous_node(self):
        if self.is_root:
            return None

        parent = self.parent

        if parent.left is self:
            return parent.previous_node

        if isnode(parent.left):
            return parent.left.rightmost

        return parent

    @property
    def next_node(self):
        if self.is_root:
            return None

        parent = self.parent

        if parent.right is self:
            return parent.next_node

        if isnode(parent.right):
            return parent.right.leftmost

        return parent

    @property
    def depth(self):
        if self.is_root:
            return 0

        return self.parent.depth + 1

    def explode(self):
        if self.depth != 4:
            return False

        previous_node, next_node = self.previous_node, self.next_node

        if previous_node:
            if isnode(previous_node.right):
                previous_node.left += self.left
            else:
                previous_node.right += self.left

        if next_node:
            if isnode(next_node.left):
                next_node.right += self.right
            else:
                next_node.left += self.right

        if self.parent.left is self:
            self.parent.left = 0
        else:
            self.parent.right = 0

        return True

    def split(self):
        left = self.left
        if not isnode(left) and left >= 10:
            self.left = BinaryNode(floor(left / 2), ceil(left / 2), parent=self)
            return True

        right = self.right
        if not isnode(right) and right >= 10:
            self.right = BinaryNode(floor(right / 2), ceil(right / 2), parent=self)
            return True

        return False

    def reduce(self):
        while (
            any(node.explode() for node in self.iter_nodes())
            or any(node.split() for node in self.iter_nodes())
        ):
            pass

    @property
    def magnitude(self):
        left = self.left.magnitude if isnode(self.left) else self.left
        right = self.right.magnitude if isnode(self.right) else self.right

        return 3 * left + 2 * right

    def copy(self):
        left = self.left.copy() if isnode(self.left) else self.left
        right = self.right.copy() if isnode(self.right) else self.right

        return BinaryNode(left, right)


def nodify(a, b):
    if isinstance(a, list):
        return nodify(nodify(*a), b)

    if isinstance(b, list):
        return nodify(a, nodify(*b))

    return BinaryNode(a, b)

SNAIL_NUMS = [nodify(*literal_eval(line)) for line in aoc_helper.day(18).splitlines()]

def snail_add(a, b):
    node = BinaryNode(a, b)
    node.reduce()

    return node

def part_one():
    return reduce(snail_add, SNAIL_NUMS).magnitude

def part_two():
    return max(
        snail_add(a.copy(), b.copy()).magnitude
        for a, b in product(SNAIL_NUMS, repeat=2)
        if a is not b
    )

aoc_helper.submit(18, part_one)
aoc_helper.submit(18, part_two)
