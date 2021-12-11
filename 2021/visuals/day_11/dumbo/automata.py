import numpy as np
from scipy.ndimage import convolve

from nurses_2.colors import gradient, AColor
from nurses_2.io import MouseButton
from nurses_2.widgets.behaviors import AutoPositionBehavior, AutoSizeBehavior
from nurses_2.widgets.graphic_widget import GraphicWidget

_KERNEL = np.ones((3, 3), dtype=int)

colorify = np.vectorize(
    gradient(
        AColor.from_hex("1a54bf"),
        AColor.from_hex("d7dd2c"),
        10,
    ).__getitem__,
    otypes=[np.uint8] * 4,
)

class Automata(AutoSizeBehavior, AutoPositionBehavior, GraphicWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset()

    def resize(self, size):
        super().resize(size)
        self.reset()

    def reset(self):
        h, w = self.size
        self._state = np.random.randint(0, 10, (2 * h, w))
        self.texture = np.dstack(colorify(self._state))

    def step(self):
        state = self._state

        state += 1

        flashed = np.zeros_like(state, dtype=bool)
        while (flashing := ((state > 9) & ~flashed)).any():
            state += convolve(flashing.astype(int), _KERNEL, mode="constant")
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
        self.texture = np.dstack(colorify(self._state))

        super().render(canvas_view, colors_view, rect)
