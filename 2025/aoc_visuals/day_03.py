import asyncio

import aoc_lube
import numpy as np
from aoc_lube.utils import int_grid
from batgrl.app import App
from batgrl.geometry import BezierCurve, Size, move_along_path

from .aoc_theme import AocText

BATTERIES = int_grid(aoc_lube.fetch(year=2025, day=3), numpy=False)


async def pack_box(box: AocText, battery: AocText, batteries: AocText):
    joltage = chr(batteries.canvas["ord"][0, 0])
    battery.is_enabled = True
    battery.pull_to_front()
    battery.set_text(joltage)
    battery.pos = batteries.pos
    battery.x -= 1

    batteries.canvas[0, :-1] = batteries.canvas[0, 1:]
    batteries.canvas["ord"][0, -1:] = ord(" ")

    box.add_str("[ ]")
    box.pos = 11, 4

    await battery.tween(duration=0.15, easing="out_cubic", x=5)
    battery.is_enabled = False
    box.add_str(f"[{joltage}]")


async def yeet(box: AocText, screen_size: Size, unused_boxes):
    vx = 100
    vy = -8 - 2 * box.y
    real_x = float(box.x)
    real_y = float(box.y)
    gravity = 100
    dt = 0.005

    while box.x < screen_size.width and box.y < screen_size.height:
        real_y += vy * dt
        real_x += vx * dt
        box.y = int(real_y)
        box.x = int(real_x)
        vy += gravity * dt
        await asyncio.sleep(0)

    if box.parent is not None:
        box.parent.remove_gadget(box)
    unused_boxes.append(box)


async def load(box: AocText, i: int):
    points = np.array([box.pos, (12 - i - 1, box.x - 2), (12 - i, 0)])
    curve = BezierCurve(points)
    await move_along_path(box, [curve], easing="in_out_circ", speed=65)


async def add_total(used_boxes: list[AocText], stack: list[int]) -> int:
    subtotal = sum(10**i * n for i, n in enumerate(reversed(stack)))
    x = 15 - len(str(subtotal))
    for box in used_boxes:
        box.canvas["ord"][0, [0, 2]] = ord(" ")

    tweens = [
        box.tween(duration=0.5, easing="out_bounce", pos=(12, i + 8 + x))
        for i, box in enumerate(used_boxes)
    ]
    await asyncio.gather(*tweens)
    await asyncio.sleep(0.3)
    return subtotal


class Visual(App):
    async def on_start(self):
        if self.root is None:
            # Just for type-checker
            return

        batteries = AocText(pos=(11, 8))
        total_label = AocText(pos=(13, 0))
        total_label.set_text(f"Joltage: {0:>15}")
        total = 0

        unused_boxes = []
        used_boxes = []
        battery = AocText(is_transparent=True, is_enabled=False)
        self.add_gadgets(batteries, battery, total_label)

        for row in BATTERIES:
            stack: list[int] = []
            batteries.set_text("".join(str(i) for i in row))
            for i, joltage in enumerate(row):
                if unused_boxes:
                    box = unused_boxes.pop()
                else:
                    box = AocText(size=(1, 3), is_transparent=True)
                self.add_gadget(box)
                await pack_box(box, battery, batteries)

                while stack and stack[-1] < joltage and 12 - len(stack) < len(row) - i:
                    stack.pop()
                    not_used = used_boxes.pop()
                    await asyncio.sleep(0.1)
                    asyncio.create_task(yeet(not_used, self.root.size, unused_boxes))

                if len(stack) < 12:
                    stack.append(joltage)
                    await load(box, len(stack))
                    used_boxes.append(box)
                else:
                    await asyncio.sleep(0.01)
                    asyncio.create_task(yeet(box, self.root.size, unused_boxes))

            total += await add_total(used_boxes, stack)
            total_label.add_str(f"Joltage: {total:>15}")

            for box in used_boxes:
                self.root.remove_gadget(box)
            unused_boxes.extend(used_boxes)
            used_boxes.clear()
