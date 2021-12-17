import asyncio
from pathlib import Path

from nurses_2.app import App
from nurses_2.io import MouseButton
from nurses_2.widgets.behaviors import AutoSizeBehavior, AutoPositionBehavior, Anchor
from nurses_2.widgets.image import Image
from nurses_2.widgets.animation import Animation
from nurses_2.widgets.parallax import Parallax

from .trajectory import Trajectory

ASSETS = Path("assets")
PARALLAX_IMAGES = sorted((ASSETS / "parallax_frames").iterdir())
POWER = .3
SCROLL_FPS = .05
SHOOT_TIMEOUT = .5


class AutoSizeParallax(AutoSizeBehavior, Parallax):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        asyncio.create_task(self._scroll())

    async def _scroll(self):
        while True:
            self.horizontal_offset += 1

            for child in self.root.children:
                if isinstance(child, Trajectory):
                    child.left -= 1

            await asyncio.sleep(SCROLL_FPS)


class AutoGeometryImage(AutoSizeBehavior, Image):
    ...


class Submarine(AutoSizeBehavior, AutoPositionBehavior, Animation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._can_shoot = True

    async def _shoot_timeout(self):
        await asyncio.sleep(SHOOT_TIMEOUT)
        self._can_shoot = True

    def on_click(self, mouse_event):
        if (
            mouse_event.button == MouseButton.NO_BUTTON
            or not self._can_shoot
        ):
            return False

        self._can_shoot = False
        asyncio.create_task(self._shoot_timeout())

        cy, cx = self.center
        cy *= 2

        y, x = self.absolute_to_relative_coords(mouse_event.position)
        y *= 2

        dx = int(POWER * (x - cx))
        dy = int(POWER * (y - cy))

        self.parent.add_widget(Trajectory(size_hint=(1.0, 2.0), dx=dx, dy=dy))
        self.parent.pull_to_front(self)


class TrickShot(App):
    async def on_start(self):
        background = AutoSizeParallax(
            layers=[AutoGeometryImage(path=path) for path in PARALLAX_IMAGES],
        )

        submarine = Submarine(
            paths=ASSETS / "submarine",
            pos_hint=(.5, .4),
            anchor=Anchor.CENTER,
            size_hint=(.4, .4),
        )

        self.root.add_widgets(background, submarine)

        submarine.play()


TrickShot().run()
