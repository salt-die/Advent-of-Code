import numpy as np
from scipy.ndimage import convolve

from nurses_2.colors import gradient, AColor, ABLACK
from nurses_2.io import MouseButton
from nurses_2.widgets.behaviors import AutoSizeBehavior
from nurses_2.widgets.graphic_widget import GraphicWidget

BLUISH = AColor.from_hex("1651aa")


class Automata(AutoSizeBehavior, GraphicWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.nstates = 10  # Octopuses flash when they reach this level.
        self.energy =   1  # Amount of energy a flashing octopus shares with each of its neighbors.

        self.reset()

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

    def resize(self, size):
        super().resize(size)
        self.reset()

    def reset(self):
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

    def on_press(self, key_press_event):
        match key_press_event.key:
            case "r" | "R":
                self.reset()
            case _:
                return False

        return True

    def on_click(self, mouse_event):
        if (
            mouse_event.button is MouseButton.NO_BUTTON
            or not self.collides_coords(mouse_event.position)
        ):
            return False

        y, x = self.absolute_to_relative_coords(mouse_event.position)
        y *= 2

        self._state[y: y + 2, x] = 0

        return True

    def render(self, canvas_view, colors_view, rect):
        self.step()
        self.texture = np.dstack(self.colorify(self._state))

        super().render(canvas_view, colors_view, rect)