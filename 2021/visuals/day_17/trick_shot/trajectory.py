import asyncio
from pathlib import Path

import cv2
import numpy as np

from nurses_2.colors import AColor
from nurses_2.widgets.graphic_widget import GraphicWidget
from nurses_2.widgets.image import Image

DRONE_PATH = Path("assets") / "drone.png"
TRAJECTORY_COLOR = AColor.from_hex("13ddd3")


class Trajectory(GraphicWidget):
    def __init__(self, *args, dx, dy, **kwargs):
        super().__init__(*args, **kwargs)

        self._dim_task = asyncio.create_task(self._dim())
        asyncio.create_task(self._shoot(dx, dy))

    async def _dim(self):
        while True:
            self.texture = (self.texture * .99).astype(np.uint8)

            try:
                await asyncio.sleep(.01)
            except asyncio.CancelledError:
                return

    async def _shoot(self, dx, dy):
        old_x = self.width // 4
        old_y = self.height

        drone = Image(pos=(old_y, old_x), path=DRONE_PATH, size_hint=(.1, .05))
        self.add_widget(drone)

        while old_y < 2 * self.height + drone.height:
            new_x, new_y = old_x + dx, old_y + dy

            cv2.line(self.texture, (old_x, old_y), (new_x, new_y), TRAJECTORY_COLOR, 2)

            dx -= 1 if dx > 0 else -1 if dx < 0 else 0
            dy += 1

            old_x, old_y = new_x, new_y
            drone.pos = new_y // 2 - drone.height // 2, new_x - drone.width // 2

            await asyncio.sleep(.1)

        while self.texture.any() and self.right > 0:
            await asyncio.sleep(.1)

        self._dim_task.cancel()
        self.parent.remove_widget(self)
