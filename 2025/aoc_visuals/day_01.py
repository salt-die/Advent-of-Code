import asyncio
from math import cos, pi, sin
from time import perf_counter

import aoc_lube
import cv2
from aoc_lube.utils import extract_ints
from batgrl.app import App
from batgrl.colors import AGREEN, ARED, AWHITE, GREEN, RED, WHITE, gradient, lerp_colors
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.graphics import Graphics
from batgrl.geometry.easings import out_cubic

from .aoc_theme import AocText

RED_GREEN = gradient(GREEN, RED, GREEN, n=100)
ROTATIONS = list(extract_ints(aoc_lube.fetch(year=2025, day=1).replace("L", "-")))


def draw_ticks(text, i):
    text.clear()
    for j in range(13):
        n = ((i % 100) - 6 + j) % 100
        text.add_str(f"{n:02}", pos=(0, 3 * j))
        if n == 0:
            text.canvas["fg_color"][0, 3 * j : 3 * j + 2] = WHITE
        else:
            text.canvas["fg_color"][0, 3 * j : 3 * j + 2] = RED_GREEN[n]


async def flash_zeros(text: AocText, n):
    start = perf_counter()
    color = GREEN if n > 0 else RED
    while True:
        current = perf_counter()
        elapsed = current - start
        if elapsed < 0.3:
            text.canvas["fg_color"] = lerp_colors(
                text.default_fg_color, color, out_cubic(elapsed / 0.3)
            )
        elif elapsed < 0.4:
            text.canvas["fg_color"] = lerp_colors(
                color, text.default_fg_color, (elapsed - 0.3) / 0.1
            )
        else:
            text.canvas["fg_color"] = text.default_fg_color
            break
        await asyncio.sleep(0)


def draw_ellipse(texture, dial):
    h, w, _ = texture.shape
    center = h // 2, w // 2
    axes = h // 2 - 5, w // 2 - 5
    end_angle = (dial % 100) / 99 * 360
    if dial // 100 % 2:
        prev_color, color = ARED, AGREEN
    else:
        prev_color, color = AGREEN, ARED
    cv2.ellipse(texture, center, axes, -90.0, 0.0, 360.0, prev_color, 2)
    cv2.ellipse(texture, center, axes, -90.0, 0.0, end_angle, color, 2)


def draw_line(texture, dial):
    m = texture.shape[0] // 2
    theta = -2 * pi * (dial % 100) / 99 + pi
    b = int(m * sin(theta) + m), int(m * cos(theta) + m)
    cv2.line(texture, (m, m), b, AWHITE, 2)


class SecretApp(App):
    async def on_start(self):
        container = Gadget(size=(21, 40), pos_hint={"x_hint": 0.5, "y_hint": 0.5})
        numbers = AocText(size=(1, 40))
        graphic = Graphics(size=(20, 40), pos=(1, 0), blitter="sixel")
        rotation = AocText(pos_hint={"x_hint": 0.5, "y_hint": 0.5}, is_transparent=True)
        zeros = AocText(pos=(1, 20), pos_hint={"x_hint": 0.5}, is_transparent=True)
        zeros.set_text("Zeros: 0")
        graphic.add_gadgets(rotation, zeros)
        container.add_gadgets(numbers, graphic)
        self.add_gadget(container)

        dial = 50
        nzeros = 0
        flash_task = None
        for n in ROTATIONS:
            rotation.set_text(f"{"L" if n < 0 else "R"}{abs(n)}")
            rotation.canvas["fg_color"][0, 0] = RED if n < 0 else GREEN
            for _ in range(abs(n)):
                dial += 1 if (n > 0) else -1
                if dial % 100 == 0:
                    nzeros += 1
                    zeros.set_text(f"Zeros: {nzeros}")
                    if flash_task is not None:
                        flash_task.cancel()
                    flash_task = asyncio.create_task(flash_zeros(zeros, n))
                draw_ticks(numbers, dial)
                graphic.texture[:] = 0
                draw_ellipse(graphic.texture, dial)
                draw_line(graphic.texture, dial)
                await asyncio.sleep(0.02)
            await asyncio.sleep(0.3)
