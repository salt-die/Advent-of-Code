import numpy as np
from numpy.linalg import norm

from nurses_2.widgets.graphic_widget import GraphicWidget
from nurses_2.widgets.behaviors.grabbable_behavior import GrabbableBehavior


from .camera import Camera


class DropRenderer(GrabbableBehavior, GraphicWidget):
    def __init__(self, *, aspect_ratio=True, **kwargs):
        super().__init__(**kwargs)
        self.aspect_ratio = aspect_ratio
        self.camera = Camera()
        self.drops = []
        self._render_drops()

    def on_size(self):
        super().on_size()
        self._render_drops()

    def grab_update(self, mouse_event):
        alpha = np.pi * -self.mouse_dy / self.height
        self.camera.rotate_x(alpha)

        beta = np.pi * self.mouse_dx / self.width
        self.camera.rotate_y(beta)

        self._render_drops()

    def _render_drops(self):
        texture = self.texture
        texture[:] = 0

        cam = self.camera
        cam_pos = cam.pos
        self.drops.sort(key=lambda drop: norm(cam_pos - drop.pos), reverse=True)

        for drop in self.drops:
            cam.render_cube(drop, texture, self.aspect_ratio)
