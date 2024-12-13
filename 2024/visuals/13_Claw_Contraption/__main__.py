import asyncio
from pathlib import Path
from random import randrange

from aoc_theme import AOC_THEME
from batgrl.app import App
from batgrl.colors import Color
from batgrl.gadgets.behaviors.button_behavior import ButtonBehavior
from batgrl.gadgets.graphics import Graphics
from batgrl.gadgets.grid_layout import GridLayout
from batgrl.gadgets.image import Image
from batgrl.gadgets.pane import Pane
from batgrl.texture_tools import read_texture, resize_texture

DARK_RED = Color.from_hex("840902")

ASSETS = Path(__file__).parent.parent / "assets"
ALIEN = ASSETS / "alien.png"
CLAW_OPEN = ASSETS / "claw_open.png"
CLAW_CLOSED = ASSETS / "claw_closed.png"
CLAW_ROD = ASSETS / "claw_rod.png"
SPACE = ASSETS / "space.png"
LEFT_BUTTON_UP = read_texture(ASSETS / "left_button_up.png")
LEFT_BUTTON_DOWN = read_texture(ASSETS / "left_button_down.png")
DOWN_BUTTON_UP = read_texture(ASSETS / "down_button_up.png")
DOWN_BUTTON_DOWN = read_texture(ASSETS / "down_button_down.png")


class GraphicButton(ButtonBehavior, Graphics):
    def __init__(self, up, down, move_coro, **kwargs):
        super().__init__(**kwargs)
        self.up = up
        self.down = down
        self.move_coro = move_coro
        self._task = None

    def update_down(self):
        self.texture[:] = resize_texture(
            self.down, self.texture.shape[:2], interpolation="nearest"
        )
        self._task = asyncio.create_task(self.move_coro())

    def update_hover(self):
        self.texture[:] = resize_texture(
            self.up, self.texture.shape[:2], interpolation="nearest"
        )
        if self._task is not None:
            self._task.cancel()
            self._task = None

    def update_normal(self):
        self.texture[:] = resize_texture(
            self.up, self.texture.shape[:2], interpolation="nearest"
        )
        if self._task is not None:
            self._task.cancel()
            self._task = None


class DownButton(GraphicButton):
    def update_down(self):
        self.texture[:] = resize_texture(
            self.down, self.texture.shape[:2], interpolation="nearest"
        )
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.move_coro())

    def update_hover(self):
        self.texture[:] = resize_texture(
            self.up, self.texture.shape[:2], interpolation="nearest"
        )

    def update_normal(self):
        self.texture[:] = resize_texture(
            self.up, self.texture.shape[:2], interpolation="nearest"
        )


class ClawContraptionApp(App):
    async def on_start(self):
        alien_y = 17

        aliens = [
            Image(path=ALIEN, size=(9, 18), pos=(alien_y, randrange(self.root.width)))
            for _ in range(14)
        ]

        claw_open = Image(path=CLAW_OPEN, size=(16, 28))
        claw_closed = Image(path=CLAW_CLOSED, size=(16, 28), is_enabled=False)
        claw_rod = Image(path=CLAW_ROD, size=(32, 28))
        background = Image(
            path=SPACE, size_hint={"height_hint": 1.0, "width_hint": 1.0}
        )

        def _on_pos():
            claw_open.top = claw_closed.top = claw_rod.bottom
            claw_open.x = claw_closed.x = claw_rod.x

        claw_rod.bind("pos", _on_pos)
        claw_rod.bottom = 0

        async def move_left():
            while True:
                claw_rod.x -= 1
                await asyncio.sleep(0.1)

        async def move_right():
            while True:
                claw_rod.x += 1
                await asyncio.sleep(0.1)

        async def claw_down():
            await claw_rod.tween(bottom=8, easing="out_back")

            claw_open.is_enabled = False
            claw_closed.is_enabled = True

            for alien in aliens:
                got_alien = abs(alien.center.x - claw_rod.center.x) < 3
                if got_alien:
                    break

            if got_alien:
                alien.pull_to_front()
                claw_rod.pull_to_front()
                claw_closed.pull_to_front()
                claw_open.pull_to_front()
                grid.pull_to_front()

                dy = alien.y - claw_rod.y
                dx = alien.x - claw_rod.x

                def _move_alien():
                    alien.y = claw_rod.y + dy
                    alien.x = claw_rod.x + dx

                i = claw_rod.bind("pos", _move_alien)

            await asyncio.sleep(0.1)
            await claw_rod.tween(duration=1.75, bottom=0, easing="out_elastic")

            if got_alien:
                claw_rod.unbind(i)

            claw_open.is_enabled = True
            claw_closed.is_enabled = False

            if got_alien:
                asyncio.create_task(drop_alien(alien))

        async def drop_alien(alien):
            gravity = 1 / 100
            velocity = 0
            real_y = alien.y
            while real_y < alien_y:
                velocity += gravity
                real_y += velocity
                alien.y = int(real_y)
                await asyncio.sleep(0.01)

        left_button = GraphicButton(
            LEFT_BUTTON_UP,
            LEFT_BUTTON_DOWN,
            move_left,
            size=(8, 14),
        )
        right_button = GraphicButton(
            LEFT_BUTTON_UP[:, ::-1],
            LEFT_BUTTON_DOWN[:, ::-1],
            move_right,
            size=(8, 14),
        )
        down_button = DownButton(
            DOWN_BUTTON_UP,
            DOWN_BUTTON_DOWN,
            claw_down,
            size=(8, 14),
        )
        button_bg = Pane(size_hint={"width_hint": 1.0}, bg_color=DARK_RED)

        grid = GridLayout(
            grid_columns=3,
            pos_hint={"x_hint": 0.5, "y_hint": 1.0, "anchor": "bottom"},
            is_transparent=True,
        )
        grid.add_gadgets(left_button, down_button, right_button)
        grid.size = grid.min_grid_size
        button_bg.height = grid.height + 1

        def _on_grid_pos():
            nonlocal alien_y
            alien_y = grid.y - 10
            for alien in aliens:
                alien.y = alien_y
            button_bg.y = grid.y - 1

        grid.bind("pos", _on_grid_pos)
        self.add_gadgets(background, button_bg)
        self.add_gadgets(aliens)
        self.add_gadgets(claw_rod, claw_open, claw_closed, grid)


ClawContraptionApp(title="Claw Contraption", color_theme=AOC_THEME).run()
