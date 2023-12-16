import asyncio
from itertools import cycle

import aoc_lube
from aoc_theme import AOC_CODE_GRAY, AOC_PRIMARY, AOC_THEME, WHITE, AocToggle
from batgrl.app import App
from batgrl.colors import rainbow_gradient
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text

TEXT = aoc_lube.fetch(2023, 16)
GRID = TEXT.splitlines()
H, W = len(GRID), len(GRID[0])
LIGHT_COLORS = cycle(rainbow_gradient(40))


async def light_travel(grid, total, toggle, start):
    states = set()
    positions = set()

    stack = [start]
    while stack:
        light_color = next(LIGHT_COLORS)
        new_stack = []
        for y, x, dy, dx in stack:
            if (y, x, dy, dx) in states:
                continue

            states.add((y, x, dy, dx))
            y += dy
            x += dx
            if not (0 <= y < H and 0 <= x < W):
                continue

            match GRID[y][x]:
                case "/":
                    dy, dx = -dx, -dy
                case "\\":
                    dy, dx = dx, dy
                case "|" if dx:
                    stack.append((y, x, -1, 0))
                    dy, dx = 1, 0
                case "-" if dy:
                    stack.append((y, x, 0, -1))
                    dy, dx = 0, 1

            if grid.canvas[y, x]["char"] not in "/\\-|":
                grid.canvas[y, x]["char"] = {
                    (0, 1): ">",
                    (-1, 0): "^",
                    (0, -1): "<",
                    (1, 0): "v",
                }[dy, dx]
                grid.colors[y, x, :3] = light_color

            positions.add((y, x))
            new_stack.append((y, x, dy, dx))

        stack = new_stack
        total.add_str(str(len(positions)).rjust(5), (-3, 7))
        await asyncio.sleep(0 if toggle.toggle_state == "on" else 0.05)
    return len(positions)


def grid_boundary_points():
    for y in range(H):
        yield y, -1, 0, 1
        yield y, W, 0, -1
    for x in range(W):
        yield -1, x, 1, 0
        yield H, x, -1, 0


class LavaApp(App):
    async def on_start(self):
        grid = Text()

        total_label = Text(size=(20, 13), default_color_pair=AOC_PRIMARY)
        total_label.canvas[:, 5]["char"] = "┃"
        total_label.add_str("━━━━━╋━━━━━━━", pos=(-2, 0))
        total_label.add_str("MAX", pos=(-1, 1))
        total_label.add_str("0", pos=(-1, -2))

        toggle = AocToggle("TURBO", lambda _: None, pos=(21, 2))

        sv = ScrollView(
            pos=(0, 13),
            size_hint={"height_hint": 1.0, "width_hint": 1.0, "width_offset": -13},
        )
        sv.view = grid
        self.add_gadgets(sv, total_label, toggle)

        current_max = 0
        for start in grid_boundary_points():
            grid.set_text(TEXT)
            grid.colors[..., :3] = 100
            grid.colors[..., :3][grid.canvas["char"] != "."] = WHITE
            grid.colors[..., 3:] = AOC_CODE_GRAY

            total_label.canvas[:-3] = total_label.canvas[1:-2]
            npoints = await light_travel(grid, total_label, toggle, start)

            current_max = max(npoints, current_max)
            total_label.add_str(str(current_max).rjust(5), (-1, 7))


if __name__ == "__main__":
    LavaApp(
        title="The Floor Will Be Lava",
        background_color_pair=AOC_PRIMARY,
        color_theme=AOC_THEME,
    ).run()
