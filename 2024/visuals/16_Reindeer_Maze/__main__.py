import asyncio
from heapq import heappop, heappush

import aoc_lube
from aoc_lube.utils import extract_maze
from aoc_theme import AOC_THEME, AocText
from batgrl.app import App
from batgrl.colors import WHITE, Color
from batgrl.gadgets.scroll_view import ScrollView
from batgrl.texture_tools import _composite

GRID, MAZE = extract_maze(aoc_lube.fetch(year=2024, day=16))
START, END = (139, 1), (1, 139)
RED = Color.from_hex("dd3330")
GREEN = Color.from_hex("22cc39")
DIM = Color.from_hex("444444")


def find_min_path():
    min_scores = {}
    best_seats = set()
    best_score = -1
    heap = [(0, START, (0, 1), [])]
    while heap:
        score, pos, dir, seats = heappop(heap)
        if pos == END:
            best_score = score
            best_seats.update(seats)
            continue

        for neighbor in MAZE[pos]:
            new_dir = neighbor[0] - pos[0], neighbor[1] - pos[1]
            new_score = score + 1001 ** (new_dir != dir)
            if min_scores.setdefault((neighbor, new_dir), new_score) >= new_score:
                min_scores[neighbor, new_dir] = new_score
                heappush(heap, (new_score, neighbor, new_dir, seats + [pos]))

    return best_score, len(best_seats) + 1


class ReindeerMazeApp(App):
    async def on_start(self):
        header = AocText(size_hint={"width_hint": 1.0})

        grid = AocText(size=GRID.shape)
        grid.canvas["char"] = GRID

        sv = ScrollView(
            pos=(1, 0),
            size_hint={"height_hint": 1.0, "height_offset": -1, "width_hint": 1.0},
            dynamic_bars=True,
        )
        sv.view = grid
        sv.vertical_proportion = 1.0
        self.add_gadgets(header, sv)

        header.add_str("Score: 0", truncate_str=True)
        min_scores = {}
        heap = [(0, START, (0, 1), [])]
        best_seats = set()
        while heap:
            score, pos, dir, seats = heappop(heap)
            header.add_str(f"Score: {score}", truncate_str=True)

            _composite(grid.canvas["fg_color"], DIM, 255, 0.05)
            grid.canvas["fg_color"][grid.canvas["char"] == "#"] = grid.default_fg_color
            for seat in best_seats:
                grid.canvas["fg_color"][seat] = GREEN
            for seat in seats:
                grid.canvas["fg_color"][seat] = RED
            grid.canvas["fg_color"][pos] = WHITE
            grid.canvas["char"][pos] = "O"

            if pos == END:
                best_seats.update(seats)
                continue

            for neighbor in MAZE[pos]:
                new_dir = neighbor[0] - pos[0], neighbor[1] - pos[1]
                new_score = score + 1001 ** (new_dir != dir)
                if min_scores.setdefault((neighbor, new_dir), new_score) >= new_score:
                    min_scores[neighbor, new_dir] = new_score
                    heappush(heap, (new_score, neighbor, new_dir, seats + [pos]))

            await asyncio.sleep(0)
            grid.canvas["fg_color"][pos] = DIM


ReindeerMazeApp(title="Reindeer Maze", color_theme=AOC_THEME).run()
