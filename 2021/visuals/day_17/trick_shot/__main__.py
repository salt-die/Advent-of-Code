import asyncio
from pathlib import Path

from nurses_2.app import App
from nurses_2.io import MouseButton
from nurses_2.widgets.widget_data_structures import Anchor
from nurses_2.widgets.image import Image
from nurses_2.widgets.animation import Animation
from nurses_2.widgets.parallax import Parallax

from .trajectory import Trajectory

ASSETS = Path("assets")
PARALLAX_IMAGES = sorted((ASSETS / "parallax_frames").iterdir())
POWER = .3
SCROLL_FPS = .05
SHOOT_TIMEOUT = .5


class AutoScrollParallax(Parallax):
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


class Submarine(Animation):
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

        y, x = self.to_local(mouse_event.position)
        y *= 2

        dx = int(POWER * (x - cx))
        dy = int(POWER * (y - cy))

        self.parent.add_widget(Trajectory(size_hint=(1.0, 2.0), dx=dx, dy=dy))
        self.pull_to_front()


class TrickShot(App):
    async def on_start(self):
        background = AutoScrollParallax(
            layers=[Image(path=path, size_hint=(1.0, 1.0)) for path in PARALLAX_IMAGES],
            size_hint=(1.0, 1.0),
        )

        submarine = Submarine(
            path=ASSETS / "submarine",
            pos_hint=(.5, .4),
            anchor=Anchor.CENTER,
            size_hint=(.4, .4),
        )

        self.add_widgets(background, submarine)

        submarine.play()


TrickShot(title="Trick Shot!").run()
