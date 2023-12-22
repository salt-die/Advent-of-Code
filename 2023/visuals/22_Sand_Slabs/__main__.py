import asyncio
import random
from bisect import insort
from dataclasses import dataclass

import aoc_lube
from aoc_lube.utils import extract_ints
from aoc_theme import AOC_PRIMARY, AocButton
from batgrl.app import App
from batgrl.colors import AColor

from .brick_renderer import BrickRenderer
from .cube import Cube

random.seed(0)

BRICK_COLORS = [
    AColor.from_hex(hex_code)
    for hex_code in (
        "e2be6f",
        "af9b70",
        "afaa70",
        "d6bd9a",
        "919177",
        "d3a756",
        "63440b",
        "ad7f2b",
        "705e3c",
        "261c0b",
        "606050",
        "e89e37",
    )
]


@dataclass
class Brick:
    brick: list[int, int, int, int, int, int]


def init_bricks():
    bricks = [
        Brick([*extract_ints(line)]) for line in aoc_lube.fetch(2023, 22).splitlines()
    ]
    bricks.sort(key=lambda brick: brick.brick[5])
    bricks = bricks[:200]  # re: 200, this is python afterall...

    stack = []
    for brick in bricks:
        x1, y1, z1, x2, y2, z2 = brick.brick

        color = random.choice(BRICK_COLORS)
        cubes = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    cubes.append(Cube([x, y, z], color))
        brick.cubes = cubes

        h = z2 - z1
        t1 = 1
        for r1, s1, t1, r2, s2, t2 in reversed(stack):
            if not (x2 < r1 or r2 < x1) and not (s2 < y1 or y2 < s1):
                z1 = t2 + 1
                break
        else:
            z1 = t1
        insort(stack, [x1, y1, z1, x2, y2, z1 + h], key=lambda brick: brick[5])

        brick.h = h
        brick.target = z1
        brick.velocity = 0
    return bricks


class SandApp(App):
    async def on_start(self):
        brick_renderer = BrickRenderer(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, disable_ptf=True
        )
        reset_event = asyncio.Event()
        reset_button = AocButton("RESET", reset_event.set)
        self.add_gadgets(brick_renderer, reset_button)

        bricks = init_bricks()
        cubes = [cube for brick in bricks for cube in brick.cubes]
        brick_renderer.cubes = cubes
        brick_renderer.render_cubes()

        while True:
            for brick in bricks:
                if brick.brick[2] == brick.target:
                    continue

                brick_renderer.is_animating = True

                brick.brick[2] = max(brick.target, brick.brick[2] - brick.velocity)
                brick.brick[5] = brick.brick[2] + brick.h

                for cube in brick.cubes:
                    cube.pos[-1] = brick.brick[2]
                    cube.update()

                brick.velocity += 0.1

            if not brick_renderer.is_animating:
                await reset_event.wait()

            if reset_event.is_set():
                bricks = init_bricks()
                reset_event.clear()

            cubes = [cube for brick in bricks for cube in brick.cubes]
            brick_renderer.cubes = cubes
            await asyncio.sleep(0)
            brick_renderer.is_animating = False
            brick_renderer.render_cubes()


if __name__ == "__main__":
    SandApp(title="Sand Slabs", background_color_pair=AOC_PRIMARY).run()
