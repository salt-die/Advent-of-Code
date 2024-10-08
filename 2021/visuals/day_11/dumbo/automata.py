import asyncio

import numpy as np
from scipy.ndimage import convolve

from nurses_2.colors import gradient, AColor, ABLACK
from nurses_2.io import MouseButton
from nurses_2.widgets.graphic_widget import GraphicWidget

BLUISH = AColor.from_hex("1651aa")


class Automata(GraphicWidget):
    def __init__(self, *args, default_color=ABLACK, **kwargs):
        super().__init__(*args, default_color=default_color, **kwargs)
        self.nstates = 10  # Octopuses flash when they reach this level.
        self.energy =   1  # Amount of energy a flashing octopus shares with each of its neighbors.

    def on_add(self):
        super().on_add()
        self._update_task = asyncio.create_task(self._step_forever())

    def on_remove(self):
        super().on_remove()
        self._update_task.cancel()

    @property
    def nstates(self):
        return self._nstates

    @nstates.setter
    def nstates(self, n):
        self._nstates = n

        self._gradient = gradient(
            BLUISH,
            ABLACK,
            n,
        )

        self.colorify = np.vectorize(
            lambda n: self._gradient[max(0, n)],
            otypes=[np.uint8] * 4,
        )

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, e):
        self._energy = e
        self.kernel = np.full((3, 3), e, dtype=int)
        self.kernel[1, 1] = 0

    def on_size(self):
        h, w = self.size
        self._state = np.random.randint(0, self.nstates, (2 * h, w))
        self.texture = np.dstack(self.colorify(self._state))

    def step(self):
        state = self._state

        state += 1

        flashed = np.zeros_like(state, dtype=bool)
        while (flashing := ((state >= self.nstates) & ~flashed)).any():
            state += convolve(flashing.astype(int), self.kernel, mode="constant")
            flashed |= flashing

        state[flashed] = 0

    def on_key(self, key_event):
        match key_event.key:
            case "r" | "R":
                self.on_size()
            case _:
                return False

        return True

    def on_mouse(self, mouse_event):
        if (
            mouse_event.button is MouseButton.NO_BUTTON
            or not self.collides_point(mouse_event.position)
        ):
            return False

        y, x = self.to_local(mouse_event.position)
        y *= 2

        self._state[y: y + 2, x] = 0

        return True

    async def _step_forever(self):
        while True:
            self.step()
            self.texture = np.dstack(self.colorify(self._state))

            try:
                await asyncio.sleep(0)
            except asyncio.CancelledError:
                return
