import numpy as np
from batgrl.gadgets.behaviors.grabbable import Grabbable
from batgrl.gadgets.graphics import Graphics
from numpy.linalg import norm

from .camera import Camera


class BrickRenderer(Grabbable, Graphics):
    def __init__(self, *, aspect_ratio=True, **kwargs):
        super().__init__(**kwargs)
        self.aspect_ratio = aspect_ratio
        self.camera = Camera()
        self.cubes = []
        self.is_animating = False
        self.render_cubes()

    def on_size(self):
        super().on_size()
        self.render_cubes()

    def on_mouse(self, mouse_event):
        if mouse_event.event_type == "scroll_up":
            self.camera.z_distance -= 1
            self.render_cubes()
            return True

        if mouse_event.event_type == "scroll_down":
            self.camera.z_distance += 1
            self.render_cubes()
            return True

        return super().on_mouse(mouse_event)

    def grab_update(self, mouse_event):
        theta = np.pi * -self.mouse_dx / self.height
        self.camera.rotate_z(theta)
        self.camera.translation[1] += self.mouse_dy * 0.5

        self.render_cubes()

    def render_cubes(self):
        if self.is_animating:
            return  # render_cubes will be called soon

        texture = self.texture
        texture[:] = 0

        cam = self.camera
        cam_pos = cam.pos
        self.cubes.sort(key=lambda drop: norm(cam_pos - drop.pos), reverse=True)

        for brick in self.cubes:
            cam.render_cube(brick, texture, self.aspect_ratio)
