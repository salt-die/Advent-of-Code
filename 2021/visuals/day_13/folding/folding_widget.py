import asyncio

import cv2
import numpy as np
from scipy.ndimage import convolve

from nurses_2.widgets.graphic_widget import GraphicWidget

from . import YELLOW_TO_WHITE, PAPER

def lerp(start, end, proportion):
    return int(start * (1 - proportion) + end * proportion)


class FoldingWidget(GraphicWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._paper = PAPER.astype(np.uint8)
        self._nfolds = 0

        self._kernels = [
            np.ones((13, 13)),
            np.ones((11, 11)),
            np.ones((9, 9)),
            np.ones((7, 7)),
            np.ones((5, 5)),
            np.ones((3, 3)),
            np.ones((3, 3)),
        ]

    def resize(self, size):
        super().resize(size)

        if self._nfolds < 7:
            paper = convolve(self._paper, self._kernels[self._nfolds], mode="constant")
        else:
            paper= self._paper

        h, w, _ = self.texture.shape

        resized_paper = cv2.resize(
            paper,
            (w, h),
            interpolation=self.interpolation,
        )

        self.texture[:] = self.default_color
        self.texture[resized_paper.astype(bool)] = next(YELLOW_TO_WHITE)

    async def fold(self, axis):
        self._nfolds += 1

        texture = self.texture
        copy = texture.copy()
        default_color = self.default_color

        h, w, _ = texture.shape

        match axis:
            case "x":
                length = w >> 1
                texture = np.swapaxes(texture, 0, 1)
                copy = np.swapaxes(copy, 0, 1)

                _, pw = self._paper.shape
                pw >>= 1
                self._paper = (self._paper[:, :pw] | self._paper[:, -1: pw: -1])

            case "y":
                length = h >> 1

                ph, _ = self._paper.shape
                ph >>= 1
                self._paper = (self._paper[:ph] | self._paper[-1: ph: -1])

        for proportion in np.linspace(0, 1, 25, endpoint=True):
            texture[:] = default_color
            texture[:length] = copy[:length]

            for start, end in zip(range(length + 1, length << 1), reversed(range(length))):
                i = lerp(start, end, proportion)

                mask = np.all(texture[i] == default_color, axis=-1)

                texture[i][mask] = copy[start][mask]

            await asyncio.sleep(.05)

        for h, w in np.linspace(
            (h // 2, length) if axis == "x" else (length // 2, w),
            (h // 2, w),
            15,
        ).astype(int):
            self.resize((h, w))

            await asyncio.sleep(.05)

        self.update_geometry()

    def render(self, canvas_view, colors_view, source):
        mask = np.any(self.texture != self.default_color, axis=-1)
        self.texture[mask] = next(YELLOW_TO_WHITE)

        super().render(canvas_view, colors_view, source)
