import asyncio
from collections import deque
from itertools import count, cycle

import numpy as np

from nurses_2.colors import Color, ColorPair, WHITE
from nurses_2.widgets.widget import Widget
from nurses_2.widgets.text_widget import TextWidget

from .tetrominoes import TETROMINOS, Orientation

AOC_CODE_BLUE = Color.from_hex("10101a")
AOC_GREY = Color.from_hex("cccccc")
GREY_ON_BLUE = ColorPair.from_colors(AOC_GREY, AOC_CODE_BLUE)
TIME_TO_FALL = .5
MAX_LEVEL = 20
FLASH_DELAY = .1
LOCK_DOWN_DELAY = .5
MOVE_RESET = 15
QUEUE_ID = count()


class Piece(TextWidget):
    @property
    def tetromino(self):
        return self._tetromino

    @tetromino.setter
    def tetromino(self, tetromino):
        self.is_enabled = True
        self._tetromino = tetromino
        self.size = tetromino.canvases[Orientation.UP].shape
        self.orientation = Orientation.UP

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation
        self.canvas = self._tetromino.canvases[orientation]


class Tetrish(Widget):
    def __init__(self, matrix_size=(22, 7), **kwargs):
        super().__init__(**kwargs)

        self.matrix = np.zeros(matrix_size, dtype=np.bool8)
        self.matrix_widget = TextWidget(
            size=matrix_size,
            pos_hint=(.5, .5),
            anchor="center",
            default_char=".",
            default_color_pair=GREY_ON_BLUE,
        )
        self.current_piece = Piece(default_color_pair=GREY_ON_BLUE, is_transparent=True)
        self.matrix_widget.add_widgets(self.current_piece)
        self.tetromino_generator = cycle(TETROMINOS)
        self.add_widget(self.matrix_widget)

    def on_add(self):
        super().on_add()
        self._game_task = asyncio.create_task(asyncio.sleep(0))  # dummy task
        self._lock_down_task = asyncio.create_task(asyncio.sleep(0))  # dummy task
        self._clear_lines_queue = deque()

    def on_remove(self):
        super().on_remove()
        self._game_task.cancel()
        self._lock_down_task.cancel()
        for task in self._clear_lines_queue:
            task.cancel()

    def new_game(self):
        self._game_task.cancel()
        self._lock_down_task.cancel()
        while self._clear_lines_queue:
            self._clear_lines_queue.popleft().cancel()

        self.matrix[:] = 0
        self.matrix_widget.canvas[:] = "."
        self.current_piece.is_enabled = False
        self._game_task = asyncio.create_task(self._run_game())
        self.new_piece()

    async def _run_game(self):
        while True:
            await asyncio.sleep(TIME_TO_FALL)
            self.move_current_piece(dy=1, dx=0)

    def start_lock_down(self):
        self._lock_down_task.cancel()
        self._lock_down_task = asyncio.create_task(self._lock_down_timer())

    async def _lock_down_timer(self):
        await asyncio.sleep(LOCK_DOWN_DELAY)
        self.affix_piece()

    def new_piece(self):
        self._lock_down_task.cancel()

        current_piece = self.current_piece
        current_piece.tetromino = next(self.tetromino_generator)
        current_piece.top = 0
        current_piece.left = 2

        if self.collides(0, 0):
            self.new_game()

    def collides(self, dy, dx, orientation=None):
        piece = self.current_piece
        if orientation is None:
            orientation = piece.orientation

        mino_positions = piece.tetromino.mino_positions[orientation] + piece.pos + (dy, dx)

        matrix = self.matrix

        return (
            (mino_positions < 0).any()
            or (matrix.shape <= mino_positions).any()
            or matrix[mino_positions[:, 0], mino_positions[:, 1]].any()
        )

    def rotate_current_piece(self, clockwise=True):
        current_piece = self.current_piece
        orientation = current_piece.orientation

        target_orientation = orientation.rotate(clockwise=clockwise)

        for dy, dx in current_piece.tetromino.WALL_KICKS[orientation, target_orientation]:
            if not self.collides(dy, dx, target_orientation):
                current_piece.orientation = target_orientation
                current_piece.y += dy
                current_piece.x += dx

                if self.collides(1, 0):
                    if not self._lock_down_task.done():
                        self.start_lock_down()
                else:
                    self._lock_down_task.cancel()

                break

    def move_current_piece(self, dy=0, dx=0):
        """
        Move current piece. Returns true if the move was successful else false.
        """
        if not self.collides(dy, dx):
            self._lock_down_task.cancel()
            self.current_piece.y += dy
            self.current_piece.x += dx

            if self.collides(1, 0):
                self.start_lock_down()

            return True

        if dy and self._lock_down_task.done():
            self.start_lock_down()

        return False

    def affix_piece(self):
        """
        Affix current piece to the stack.
        """
        self._lock_down_task.cancel()

        piece = self.current_piece
        mino_positions = piece.tetromino.mino_positions[piece.orientation] + piece.pos

        h, w = self.matrix.shape
        for y, x in mino_positions:
            if 0 <= y < h and 0 <= x < w:
                self.matrix[y, x] = 1
                self.matrix_widget.canvas[y, x] = "#"

        task_name = str(next(QUEUE_ID))
        self._clear_lines_queue.append(
            asyncio.create_task(self.clear_lines(task_name), name=task_name)
        )
        self.new_piece()

    async def clear_lines(self, task_name):
        """
        Clear completed lines.
        """
        # To prevent multiple line clears from interfering with each
        # other they are run sequentially:
        queue = self._clear_lines_queue

        while queue[0].get_name() != task_name:
            if queue[0].done():
                queue.popleft()
            else:
                await queue[0]

        matrix = self.matrix
        completed_lines = np.all(matrix, axis=1)

        if not completed_lines.any():
            return

        not_completed_lines = np.any(~matrix, axis=1)
        matrix_canvas = self.matrix_widget.canvas
        matrix_colors = self.matrix_widget.colors
        old_colors = matrix_colors[completed_lines].copy()

        delay = FLASH_DELAY
        for _ in range(10):
            matrix_colors[completed_lines, ..., :3] = WHITE
            await asyncio.sleep(delay)

            delay *= .8
            matrix_colors[completed_lines] = old_colors
            await asyncio.sleep(delay)

        nlines = completed_lines.sum()

        matrix[nlines:] = matrix[not_completed_lines]
        matrix[:nlines] = 0

        matrix_canvas[nlines:] = matrix_canvas[not_completed_lines]
        matrix_canvas[:nlines] = "."
        matrix_colors[nlines:] = matrix_colors[not_completed_lines]

        self._lock_down_task.cancel()

    def drop_current_piece(self):
        """
        Drop piece.
        """
        while self.move_current_piece(dy=1):
            pass

    def on_key(self, key_event):
        match key_event.key:
            case "right" | "6":
                self.move_current_piece(dx=1)
            case "left" | "4":
                self.move_current_piece(dx=-1)
            case "down" | "2":
                if not self.move_current_piece(dy=1):
                    self.affix_piece()
            case " " | "8":
                self.drop_current_piece()
            case "z" | "1" | "5" | "9":
                self.rotate_current_piece(clockwise=False)
            case "x" | "up" | "3" | "7":
                self.rotate_current_piece()
            case _:
                return False

        return True
