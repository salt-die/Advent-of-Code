import asyncio
from heapq import heappop, heappush

import aoc_lube
from aoc_lube.utils import int_grid
from aoc_theme import AOC_CODE_BLOCK, AOC_PRIMARY, AOC_THEME, AocToggle
from batgrl.app import App
from batgrl.colors import Color, lerp_colors
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.gadgets.text import Text

TEXT = aoc_lube.fetch(year=2023, day=17)
GRID = int_grid(TEXT)
H, W = GRID.shape
ARROWS = {(0, 1): ">", (-1, 0): "^", (0, -1): "<", (1, 0): "v"}
RED = Color.from_hex("dd3330")
GREEN = Color.from_hex("22cc39")


async def min_heatloss(mn, mx, grid, heap_label, toggle):
    path_label = grid.children[0]
    heap = [(0, ((0, 0, 1, 0),)), (0, ((0, 0, 0, 1),))]
    heatlosses = {}
    while heap:
        # Repaint heap
        tmp_heap = []
        heap_label.canvas["char"][3:] = " "
        for i in range(min(18, len(heap))):
            item = heappop(heap)
            tmp_heap.append(item)
            heatloss, (*_, (y, x, dy, dx)) = item

            heap_label.add_str(
                f"{heatloss} ({y}, {x}) {ARROWS[dy, dx]}", pos=(i + 3, 0)
            )
        # Fix heap
        while tmp_heap:
            heappush(heap, tmp_heap.pop())

        heatloss, path = heappop(heap)

        # Paint path
        path_label.canvas["char"] = " "
        grid.colors[..., :3][grid.colors[..., :3] < 250] += 5
        _heatloss = 0
        for y, x, dy, dx in path:
            _heatloss += GRID[y, x]
            path_label.canvas["char"][y, x] = ARROWS[dy, dx]
            grid.colors[y, x, :3] = path_label.colors[y, x, :3] = lerp_colors(
                GREEN, RED, _heatloss / 900
            )

        if y == H - 1 and x == W - 1:
            return heatloss

        for dy, dx in ((-dx, dy), (dx, -dy)):
            Δheatloss = 0
            new_path = ()
            for d in range(1, mx + 1):
                v = y + dy * d
                u = x + dx * d

                if not (0 <= v < H and 0 <= u < W):
                    break

                new_path += ((v, u, dy, dx),)
                Δheatloss += GRID[v, u]

                if d >= mn:
                    new_heatloss = heatloss + Δheatloss
                    if heatlosses.get((v, u, dy, dx), float("inf")) > new_heatloss:
                        heatlosses[v, u, dy, dx] = new_heatloss
                        heappush(heap, (new_heatloss, path + new_path))

        await asyncio.sleep(0 if toggle.toggle_state == "on" else 0.1)


class CrucibleApp(App):
    async def on_start(self):
        grid = Text(default_color_pair=AOC_CODE_BLOCK)
        grid.set_text(TEXT)
        path_label = Text(
            size=grid.size, default_color_pair=AOC_CODE_BLOCK, is_transparent=True
        )
        grid.add_gadget(path_label)

        stack_label = Text(size=(21, 20), default_color_pair=AOC_PRIMARY)
        stack_label.add_str("HEAP".center(20))
        stack_label.add_str("━" * 20, pos=(1, 0))
        stack_label.add_str("COST (Y, X) DIR", pos=(2, 0))

        toggle = AocToggle("TURBO", lambda _: None, pos=(21, 2))

        sv = ScrollView(
            pos=(0, 20),
            size_hint={"height_hint": 1.0, "width_hint": 1.0, "width_offset": -20},
        )
        sv.view = grid
        self.add_gadgets(sv, stack_label, toggle)

        await min_heatloss(4, 10, grid, stack_label, toggle)


if __name__ == "__main__":
    CrucibleApp(
        title="Clumsy Crucible",
        background_color_pair=AOC_PRIMARY,
        color_theme=AOC_THEME,
    ).run()
