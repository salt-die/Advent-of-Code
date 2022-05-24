"""
Stable fluid simulation.
"""
from itertools import cycle

import numpy as np
from scipy.ndimage import map_coordinates
from scipy.ndimage.filters import convolve

from nurses_2.colors import rainbow_gradient, ABLACK
from nurses_2.data_structures import Point
from nurses_2.io import MouseEvent, MouseButton
from nurses_2.widgets.graphic_widget import GraphicWidget

DIF_KERNEL = np.array([-.5, 0.0, .5])
GRAD_KERNEL = np.array([-1.0, 0.0, 1.0])
GAUSSIAN_KERNEL = np.array([
    [.0625, .125, .0625],
    [ .125,  .25,  .125],
    [.0625, .125, .0625],
])
PRESSURE_KERNEL = np.array([
    [0.0, .25, 0.0],
    [.25, 0.0, .25],
    [0.0, .25, 0.0],
])
CURL = 6.0
POKE_RADIUS = 3.0
DISSIPATION = .99
PRESSURE = .6
PRESSURE_ITERATIONS = 10
RAINBOW_COLORS = cycle(rainbow_gradient(100))
EPSILON = np.finfo(float).eps


class StableFluid(GraphicWidget):
    def __init__(self, *args, default_color=ABLACK, **kwargs):
        super().__init__(*args, default_color=default_color, **kwargs)
        self.on_size()

    def on_size(self):
        h, w = self._size
        h *= 2

        self.texture = np.full((h, w, 4), self.default_color, dtype=np.uint8)
        self.dye = np.zeros((3, h, w))
        self.indices = np.indices((h, w))
        self.velocity = np.zeros((2, h, w))

    def poke(self, pos: Point | None=None):
        y, x = pos or self.center
        y *= 2

        ys, xs = self.indices
        ry = ys - y
        rx = xs - x
        d = ry**2 + rx**2 + EPSILON

        self.velocity[0] += ry / d
        self.velocity[1] += rx / d

        poke_force = np.e**(-d / POKE_RADIUS)
        self.dye += np.moveaxis(poke_force[..., None] * next(RAINBOW_COLORS), -1, 0)

    def on_click(self, mouse_event: MouseEvent):
        """
        Add dye on click.
        """
        if (
            mouse_event.button is MouseButton.NO_BUTTON
            or not self.collides_point(mouse_event.position)
        ):
            return False

        self.poke(
            self.to_local(mouse_event.position),
        )

        return True

    def render(self, canvas_view, colors_view, source: tuple[slice, slice]):
        vy, vx = velocity = self.velocity

        # Vorticity
        ###########
        div_y = convolve(vy, DIF_KERNEL[None])
        div_x = convolve(vx, DIF_KERNEL[:, None])

        curl = div_y - div_x

        vort_y = convolve(curl, DIF_KERNEL[None])
        vort_x = convolve(curl, DIF_KERNEL[:, None])

        vorticity = np.stack((vort_x, vort_y))
        vorticity /= np.linalg.norm(vorticity, axis=0) + EPSILON
        vorticity *= curl * CURL

        velocity += vorticity

        # Pressure Solver
        #################
        div = .25 * (div_y + div_x)

        pressure = np.full_like(div_y, PRESSURE)
        for _ in range(PRESSURE_ITERATIONS):
            convolve(pressure, PRESSURE_KERNEL, output=pressure, mode="constant")
            pressure -= div

        # Project
        #########
        vy -= convolve(pressure, GRAD_KERNEL[None])
        vx -= convolve(pressure, GRAD_KERNEL[:, None])

        # Advect
        ########
        coords = self.indices - velocity

        map_coordinates(vy, coords, output=vy, prefilter=False)
        map_coordinates(vx, coords, output=vx, prefilter=False)

        # Remove checkerboard divergence and diffuse velocity.
        convolve(vy, GAUSSIAN_KERNEL, output=vy, mode="constant")
        convolve(vx, GAUSSIAN_KERNEL, output=vx, mode="constant")

        r, g, b = dye = self.dye
        map_coordinates(r, coords, output=r)
        map_coordinates(g, coords, output=g)
        map_coordinates(b, coords, output=b)

        dye *= DISSIPATION
        np.clip(dye, 0, 255, out=dye)

        self.texture[..., :3] = np.moveaxis(dye, 0, -1)

        super().render(canvas_view, colors_view, source)
