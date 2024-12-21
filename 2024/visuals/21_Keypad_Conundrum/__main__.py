import asyncio
from functools import cache
from itertools import starmap
from time import perf_counter

from aoc_lube.utils import sliding_window
from aoc_theme import AOC_THEME, AocButton, AocText
from batgrl.app import App
from batgrl.colors import WHITE, Color, lerp_colors
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.grid_layout import GridLayout
from batgrl.gadgets.pane import Pane
from batgrl.gadgets.textbox import Textbox
from batgrl.geometry.easings import out_exp

GREEN = Color.from_hex("22cc39")
RED = Color.from_hex("dd3330")


def make_keys(keys):
    return {key: (y, x) for y, row in enumerate(keys) for x, key in enumerate(row)}


KEYPAD = make_keys(["789", "456", "123", "_0A"])
KEYPAD_COORDS = {v: k for k, v in KEYPAD.items()}
ARROWS = make_keys(["_^A", "<v>"])
ARROWS_COORDS = {v: k for k, v in ARROWS.items()}
NUMPAD = {
    key: (y, x)
    for y, row in enumerate(["789", "456", "123", "_0A", "<v>"])
    for x, key in enumerate(row)
}
NUMPAD["^"] = NUMPAD["0"]
_Y, _X = NUMPAD["_"]
DELAY = 0.01


@cache
def paths(a, b):
    (uy, ux), (vy, vx) = NUMPAD[a], NUMPAD[b]
    dy, dx = vy - uy, vx - ux
    path = f"{'v' * dy}{'^' * -dy}{'>' * dx}{'<' * -dx}"
    paths = []
    if ux != _X or vy != _Y:
        paths.append(f"{path}A")
    if dy and dx and (uy != _Y or vx != _X):
        paths.append(f"{path[::-1]}A")
    return paths


@cache
def keys(code, nrobots=2):
    all_paths = starmap(paths, sliding_window("A" + code))
    if nrobots == 0:
        return "".join(path[0] for path in all_paths)
    return "".join(
        min((keys(path, nrobots - 1) for path in paths), key=len) for paths in all_paths
    )


async def flash_robot(robot, color, duration=1):
    start = perf_counter()
    half = duration / 2

    while True:
        now = perf_counter()
        elapsed = now - start
        if elapsed > duration:
            break

        if elapsed > half:
            robot.bg_color = lerp_colors(color, GREEN, out_exp((elapsed - half) / half))
        else:
            robot.bg_color = lerp_colors(GREEN, color, out_exp(elapsed / half))
        await asyncio.sleep(0)
    robot.bg_color = GREEN


class OnlyInts(Textbox):
    def on_key(self, key_event):
        if len(key_event.key) == 1 and not (
            key_event.key.isdigit() or key_event.key == "A" or key_event.ctrl
        ):
            return

        return super().on_key(key_event)


class KeypadButton(ButtonBehavior, AocText):
    def __init__(self, key, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.set_text(f"+---+\n| {key} |\n+---+")

    def update_theme(self):
        super().update_theme()
        self.update_normal()

    def update_normal(self):
        self.canvas["char"][[0, -1], 1:-1] = "-"
        self.canvas["fg_color"][1, 2] = self.color_theme.button_normal.fg

    def update_hover(self):
        self.canvas["char"][[0, -1], 1:-1] = "-"
        self.canvas["fg_color"][1, 2] = self.color_theme.button_hover.fg

    def update_down(self):
        self.canvas["char"][[0, -1], 1:-1] = "_"

    def on_release(self):
        self.parent.parent.update_label(self.key)


class Keypad(Gadget):
    robot_id = 0
    robots = []

    def __init__(self, keys, key_coords, **kwargs):
        super().__init__(**kwargs)
        self.keys = keys
        self.key_coords = key_coords
        self.label = AocText(size=(1, 13))

        ky, kx = keys["A"]
        self.driver = Pane(
            bg_color=GREEN,
            alpha=0.25,
            size=(3, 5),
            pos=(2 * ky + 1, 4 * kx),
            is_enabled=False,
        )
        self.robots.append(self.driver)
        self.robot_id = Keypad.robot_id
        if self.robot_id:
            self.driven = self.robots[self.robot_id - 1]
            self.driven.is_enabled = True
        else:
            self.driven = None

        Keypad.robot_id += 1

        grid = GridLayout(
            pos=(1, 0),
            grid_rows=len(keys) // 3,
            grid_columns=3,
            horizontal_spacing=-1,
            vertical_spacing=-1,
        )
        for key in keys:
            if key == "_":
                grid.add_gadget(Gadget(size=(3, 5), is_transparent=True))
            else:
                grid.add_gadget(KeypadButton(key))

        grid.size = grid.min_grid_size
        self.size = grid.height + 1, 13
        self.add_gadgets(self.label, grid, self.driver)
        self._flash_task = None

    def update_label(self, key):
        self.label.canvas["char"][0, :-1] = self.label.canvas["char"][0, 1:]
        self.label.canvas["char"][0, -1] = key
        if self.driven:
            robot_key = self.robot_key()
            if key == "A":
                self.driven.parent.update_label(robot_key)
                if self._flash_task is not None:
                    self._flash_task.cancel()
                self._flash_task = asyncio.create_task(flash_robot(self.driven, WHITE))
            elif key == "<":
                self.move_robot(0, -1)
            elif key == "v":
                self.move_robot(1, 0)
            elif key == ">":
                self.move_robot(0, 1)
            elif key == "^":
                self.move_robot(-1, 0)

    def robot_key(self):
        y, x = self.driven.pos
        keypos = (y - 1) // 2, x // 4
        return self.driven.parent.key_coords.get(keypos)

    def move_robot(self, dy, dx):
        y, x = self.driven.pos
        ky, kx = (y - 1) // 2, x // 4
        nky, nkx = ky + dy, kx + dx
        self.driven.pos = 2 * nky + 1, 4 * nkx
        key = self.robot_key()
        if not key or key == "_":
            self.driven.pos = y, x
            if self._flash_task is not None:
                self._flash_task.cancel()
            self._flash_task = asyncio.create_task(flash_robot(self.driven, RED))


class KeypadConundrumApp(App):
    async def on_start(self):
        start_event = asyncio.Event()

        numpad = Keypad(KEYPAD, KEYPAD_COORDS)
        arrows_1 = Keypad(ARROWS, ARROWS_COORDS)
        arrows_2 = Keypad(ARROWS, ARROWS_COORDS)
        arrows_3 = Keypad(ARROWS, ARROWS_COORDS)

        keygrid = GridLayout(grid_columns=4, pos=(2, 0), horizontal_spacing=2)
        keygrid.add_gadgets(numpad, arrows_1, arrows_2, arrows_3)
        keygrid.size = keygrid.min_grid_size

        textbox = OnlyInts(size=(1, 8))

        def do_reset():
            start_event.clear()
            for keypad in keygrid.children:
                keypad.children[0].clear()
                ky, kx = keypad.keys["A"]
                keypad.children[2].pos = 2 * ky + 1, 4 * kx

        reset_button = AocButton("Reset", do_reset)

        def do_start():
            do_reset()
            start_event.set()

        start_button = AocButton("Start", do_start)
        header = GridLayout(grid_columns=3)
        header.add_gadgets(textbox, reset_button, start_button)
        header.size = header.min_grid_size
        self.add_gadgets(header, keygrid)

        while True:
            await start_event.wait()
            driver = arrows_3.driver
            driver.is_enabled = True
            driver.alpha = 0
            iy, ix = arrows_3.keys["A"]
            driver.pos = 2 * iy + 1, 4 * ix
            await driver.tween(alpha=0.25, duration=DELAY * 5)

            code = keys(textbox.text)
            for key in code:
                y, x = driver.pos
                ky, kx = arrows_3.keys[key]
                ny, nx = 2 * ky + 1, 4 * kx
                a = driver.tween(y=ny, duration=abs(ny - y) * DELAY)
                b = driver.tween(x=nx, duration=abs(nx - x) * DELAY)
                if (y - 1) // 2 or nx:
                    a, b = b, a
                await a
                await b
                arrows_3.update_label(key)
                await flash_robot(driver, WHITE, DELAY * 10)

                await asyncio.sleep(DELAY)
                if not start_event.is_set():
                    break

            await driver.tween(alpha=0, duration=DELAY * 5)
            driver.is_enabled = False
            start_event.clear()


KeypadConundrumApp(
    title="Keypad Conundrum", color_theme=AOC_THEME, inline=True, inline_height=12
).run()
