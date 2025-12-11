import asyncio

import aoc_lube
import numpy as np
from aoc_lube.utils import extract_ints
from batgrl.app import App
from batgrl.colors import GREEN, RED, WHITE, rainbow_gradient
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.grid_layout import GridLayout
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.geometry import clamp

from .aoc_theme import AocText, AocToggle

RAW = aoc_lube.fetch(year=2025, day=10)


def parse_raw():
    for line in RAW.splitlines():
        lights, *buttons, _ = line.split()
        yield lights, list(tuple(extract_ints(button)) for button in buttons)


DATA: list[tuple[str, list[tuple[int, ...]]]] = list(parse_raw())


def line_char(dy, dx, turn):
    if dy == 0:
        return "─"
    if dx == 0:
        return "│"
    if dx > 0:
        if dy > 0:
            return "╰╮"[turn]
        return "╭╯"[turn]
    if dy > 0:
        return "╯╭"[turn]
    return "╮╰"[turn]


def draw_path(start, end, turn, color, canvas):
    h, w = canvas.shape
    cy, cx = start
    ey, ex = end
    dy = (ey > cy) - (cy > ey)
    dx = (ex > cx) - (cx > ex)
    while cy != turn:
        cy += dy
        if 0 <= cy < h and 0 <= cx < w:
            canvas[cy, cx]["ord"] = ord("│")
            canvas[cy, cx]["fg_color"] = color
    if 0 <= cy < h and 0 <= cx < w:
        canvas[cy, cx]["ord"] = ord(line_char(dy, dx, 0))
    while cx != ex:
        cx += dx
        if 0 <= cy < h and 0 <= cx < w:
            canvas[cy, cx]["ord"] = ord("─")
            canvas[cy, cx]["fg_color"] = color
    if 0 <= cy < h and 0 <= cx < w:
        canvas[cy, cx]["ord"] = ord(line_char(dy, dx, 1))
    while cy != ey:
        cy += dy
        if 0 <= cy < h and 0 <= cx < w:
            canvas[cy, cx]["ord"] = ord("│")
            canvas[cy, cx]["fg_color"] = color


def button_label(button) -> str:
    if len(button) == 1:
        return f" {button[0]} "
    return f" {str(button)[1:-1]} "


def make_button_callback(button, lights, event):
    def callback(_):
        ords = lights.canvas["ord"]
        for i in button:
            if ords[1, i + 1] == ord("#"):
                ords[1, i + 1] = ord(".")
            else:
                ords[1, i + 1] = ord("#")
        if (ords[0] == ords[1]).all():
            event.set()

    return callback


class LightButton(AocToggle):
    def __init__(self, button, lights, wires, event):
        self._button = button
        self._wires = wires
        self._event = event

        super().__init__(
            "", make_button_callback(button, lights, event), is_transparent=True
        )

        if len(button) == 1:
            label = f"({button[0]})"
        else:
            label = str(button)

        self.set_text(label)

    def update_hover(self):
        super().update_hover()
        self._wires.draw_wires()

    def update_down(self):
        super().update_down()
        self.canvas["fg_color"] = WHITE
        self._wires.draw_wires()

    def update_normal(self):
        self.canvas["style"] = 0
        if self.toggle_state == "off":
            self.update_off()
        else:
            self.update_on()

    def update_on(self):
        self.canvas["fg_color"] = GREEN
        self._wires.draw_wires()

    def update_off(self):
        self.canvas["fg_color"] = RED
        self._wires.draw_wires()


class Wires(AocText):
    def __init__(self, lights, buttons, **kwargs):
        super().__init__(**kwargs)
        self._lights = lights
        self._buttons = buttons

    def _draw_wires(self, button, color):
        for i, light in enumerate(button._button):
            draw_path(
                (10, button.x + 1 + 3 * i),
                (0, self._lights.x + 1 + light),
                2 + i,
                color,
                self.canvas,
            )

    def draw_wires(self):
        self.clear()
        for button in self._buttons:
            if button.toggle_state == "on":
                self._draw_wires(button, GREEN)

        for button in self._buttons:
            if button.button_state == "hover":
                self._draw_wires(button, button.get_color("button_hover_fg"))
            elif button.button_state == "down":
                self._draw_wires(button, WHITE)

    async def glow(self):
        self.canvas["fg_color"] = GREEN
        colors = self.canvas["fg_color"]
        N = 10
        grad = np.array(rainbow_gradient(N))
        for i in range(self.height - 1, -N, -1):
            if i >= 0:
                h = clamp(self.height - i, 1, N)
                colors[i : i + h] = grad[:h, None]
                colors[:i] = GREEN
            else:
                colors[: N + i] = grad[-N - i :, None]
                colors[N + i :] = GREEN
            await asyncio.sleep(0.04)


class Visual(App):
    async def on_start(self):
        container = Gadget(size=(13, 1))
        sv = ScrollView(size=(14, 1), pos_hint={"x_hint": 0.5}, dynamic_bars=True)
        sv.view = container
        self.add_gadget(sv)

        def fix_sv_size():
            assert self.root

            if container.width < self.root.width:
                sv.width = container.width
            else:
                sv.width = self.root.width

        assert self.root
        self.root.bind("size", fix_sv_size)
        container.bind("size", fix_sv_size)

        lights_label = AocText(pos_hint={"x_hint": 0.5})

        button_gadgets = []
        wires = Wires(lights_label, button_gadgets, pos=(2, 0), size=(10, 1))

        grid = GridLayout(pos=(12, 0), grid_rows=1)
        container.add_gadgets(lights_label, wires, grid)

        lights_event = asyncio.Event()

        for lights, buttons in DATA:
            grid.grid_columns = len(buttons)
            buttons.sort(key=len)
            for button in buttons:
                button_gadget = LightButton(button, lights_label, wires, lights_event)
                button_gadgets.append(button_gadget)

            grid.add_gadgets(button_gadgets)
            grid.size = grid.min_grid_size
            container.width = wires.width = grid.width

            x = sv.x
            sv.x = -sv.width
            await sv.tween(easing="out_bounce", duration=0.75, x=x)

            await lights_event.wait()
            await wires.glow()
            await sv.tween(easing="out_bounce", duration=0.75, x=self.root.width)

            grid.prolicide()
            button_gadgets.clear()
            wires.clear()
            lights_event.clear()
            lights_label.set_text(f"{lights}\n[{"." * (len(lights) - 2)}]")
