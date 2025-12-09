import asyncio
from itertools import combinations

import numpy as np
from batgrl.app import App
from batgrl.colors import BLUE, GREEN, RED, WHITE
from batgrl.gadgets.cursor import Cursor
from batgrl.gadgets.pane import Pane
from batgrl.geometry import Point, Pointlike
from batgrl.text_tools import Style, new_cell
from cv2 import fillPoly, line, polylines
from shapely import Polygon

from .aoc_theme import AocButton, AocText


def area(a: Pointlike, b: Pointlike) -> int:
    ay, ax = a
    by, bx = b
    return (abs(ay - by) + 1) * (abs(ax - bx) + 1)


def rect(a: Pointlike, b: Pointlike) -> Polygon:
    ay, ax = a
    by, bx = b
    return Polygon([a, (ay, bx), b, (by, ax)])


class PolygonCanvas(AocText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points: list[Point] = []

        self._buffer = np.zeros(self.size, dtype=np.uint8)
        """A contiguous array for cv functions to draw in."""
        self.line_canvas = AocText(
            size_hint={"height_hint": 1.0, "width_hint": 1.0}, is_transparent=True
        )

        self.cursor = Cursor(bold=True, fg_color=RED, is_enabled=False)

        self._find_max_rect_task: asyncio.Task | None = None
        self._rect = Pane(is_enabled=False, alpha=0.5)
        self._max_rect = Pane(is_enabled=False, bg_color=BLUE, alpha=0.5)

        def new_region():
            if self._find_max_rect_task is not None:
                self._find_max_rect_task.cancel()
            self._rect.is_enabled = False
            self._max_rect.is_enabled = False
            self.new_region_button.is_enabled = False

            self.cursor.is_enabled = True
            self.points.clear()
            self.clear()

        self.new_region_button = AocButton(
            label="New Region", callback=new_region, pos_hint={"x_hint": 0.5}
        )

        self.add_gadgets(
            self._rect,
            self._max_rect,
            self.line_canvas,
            self.cursor,
            self.new_region_button,
        )

    def on_size(self):
        super().on_size()
        self._buffer = np.zeros(self.size, dtype=np.uint8)

    def on_mouse(self, mouse_event) -> bool | None:
        if not self.cursor.is_enabled:
            return

        if not self.collides_point(mouse_event.pos):
            return

        a = self.to_local(mouse_event.pos)
        self.cursor.pos = a
        self.update_line(a)
        if self.point_ok(a):
            self.line_canvas.canvas["fg_color"] = WHITE
            self.line_canvas.canvas["style"] = Style.BOLD

            if mouse_event.event_type == "mouse_down":
                self.points.append(a)
                self.update_rectilinear_region()

    def point_ok(self, a: Point) -> bool:
        if not self.points:
            return True

        if len(self.points) == 1:
            b = self.points[-1]
            if a.y == b.y or a.x == b.x:
                return True
            return False

        c, b = self.points[-2:]
        return c.x == b.x and b.y == a.y or c.y == b.y and b.x == a.x

    def update_line(self, a: Point):
        if not self.points:
            return

        self.line_canvas.clear()
        self._buffer[:] = 0
        b = self.points[-1]
        line(self._buffer, a[::-1], b[::-1], 1)
        self._buffer[b] = 0
        self.line_canvas.canvas["ord"][np.nonzero(self._buffer)] = ord("O")

    def update_rectilinear_region(self):
        self.line_canvas.clear()

        self._buffer[:] = 0
        if len(self.points) >= 4 and self.points[0] == self.points[-1]:
            self.cursor.is_enabled = False
            fillPoly(self._buffer, [np.array([(x, y) for y, x in self.points])], 1)
            self._find_max_rect_task = asyncio.create_task(self.find_max_rect())
        else:
            polylines(
                self._buffer, [np.array([(x, y) for y, x in self.points])], False, 1
            )

        where = np.nonzero(self._buffer)
        self.canvas["fg_color"][where] = GREEN
        self.canvas["ord"][where] = ord("X")

        ys, xs = zip(*self.points)
        self.canvas["ord"][ys, xs] = ord("#")
        self.canvas["fg_color"][ys, xs] = RED

    async def find_max_rect(self):
        self._rect.is_enabled = True

        del self.points[-1]
        polygon = Polygon(self.points)
        max_area = 0

        for a, b in combinations(self.points, 2):
            y1, x1 = a
            y2, x2 = b
            top_left = min(y1, y2), min(x1, x2)
            h, w = abs(y1 - y2) + 1, abs(x1 - x2) + 1

            self._rect.pos = top_left
            self._rect.size = h, w

            if polygon.contains(rect(a, b)):
                self._rect.bg_color = GREEN
                rect_area = h * w
                if rect_area > max_area:
                    max_area = rect_area
                    self._max_rect.pos = top_left
                    self._max_rect.size = h, w
                    self._max_rect.is_enabled = True
            else:
                self._rect.bg_color = RED

            await asyncio.sleep(0.05)

        self._rect.is_enabled = False
        self.new_region_button.is_enabled = True
        self.new_region_button.button_state = "normal"
        self.new_region_button.update_normal()


class Visual(App):
    async def on_start(self):
        assert self.root  # For type-checker

        poly_canvas = PolygonCanvas(
            size_hint={"height_hint": 1.0, "width_hint": 1.0},
            default_cell=new_cell(ord=ord(".")),
        )
        self.add_gadget(poly_canvas)
