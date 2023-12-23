import asyncio
from itertools import cycle

from aoc_lube.utils import GRID_NEIGHBORHOODS
from aoc_theme import AOC_PRIMARY
from batgrl.app import App
from batgrl.colors import rainbow_gradient
from batgrl.gadgets.gadget import Gadget
from batgrl.gadgets.text import Text

RAINBOW = cycle(rainbow_gradient(40))
EXAMPLE = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
GRID = EXAMPLE.splitlines()
H, W = len(GRID), len(GRID[0])


class WalkApp(App):
    async def on_start(self):
        path_label = Text(is_transparent=True)

        grid = Text(default_color_pair=AOC_PRIMARY)
        grid.set_text(EXAMPLE)
        grid.add_gadget(path_label)
        path_label.size = grid.size

        path_length_label = Text(default_color_pair=AOC_PRIMARY)
        path_length_label.top = grid.bottom
        path_length_label.size = 1, W

        container = Gadget(
            pos_hint={"y_hint": 0.5, "x_hint": 0.5}, background_color_pair=AOC_PRIMARY
        )
        container.size = H + 1, W
        container.add_gadgets(grid, path_length_label)

        self.add_gadget(container)

        forwards = [[(0, 1)]]
        i = 0
        while forwards:
            path_length_label.add_str(f"Path Length: {i}".center(W))

            color = next(RAINBOW)
            new_forwards = []
            to_remove = []
            for path in forwards:
                y, x = path[-1]
                path_label.colors[y, x, :3] = color

                if len(path) == 1:
                    path_label.canvas["char"][y, x] = "S"
                    ldy, ldx = 1, 0
                else:
                    path_label.canvas["char"][y, x] = "O"
                    ly, lx = path[-2]
                    ldy, ldx = y - ly, x - lx

                continued = False
                for dy, dx in GRID_NEIGHBORHOODS[4]:
                    ny, nx = y + dy, x + dx
                    if (
                        (dy, dx) != (-ldy, -ldx)
                        and 0 <= ny < H
                        and 0 <= nx < W
                        and GRID[ny][nx] != "#"
                    ):
                        if GRID[ny][nx] == ">" and dx == -1:
                            continue
                        if GRID[ny][nx] == "<" and dx == 1:
                            continue
                        if GRID[ny][nx] == "^" and dy == 1:
                            continue
                        if GRID[ny][nx] == "v" and dy == -1:
                            continue
                        continued = True
                        new_forwards.append(path + [(ny, nx)])

                if not continued and len(forwards) > len(to_remove) + 1:
                    to_remove.append(path)

            for path in to_remove:
                forwards.remove(path)

            for path in to_remove:
                points = set(path)
                for other in forwards:
                    points.difference_update(other)
                for y, x in points:
                    path_label.canvas["char"][y, x] = " "

            forwards = new_forwards
            i += 1
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    WalkApp(title="A Long Walk", background_color_pair=AOC_PRIMARY).run()
