import numpy as np

CUBE_WIDTH = 0.9


class Cube:
    __slots__ = "pos", "face_pos", "vertices", "normals", "color"

    faces = (
        (0, (0, 0, 1, 1), (0, 1, 1, 0)),
        (1, (0, 0, 1, 1), (0, 1, 1, 0)),
        ((0, 1, 1, 0), 0, (0, 0, 1, 1)),
        ((0, 1, 1, 0), 1, (0, 0, 1, 1)),
        ((0, 0, 1, 1), (0, 1, 1, 0), 0),
        ((0, 0, 1, 1), (0, 1, 1, 0), 1),
    )

    def __init__(self, pos, color):
        self.pos = np.array(pos, dtype=float)
        self.color = color
        self.normals = np.array(
            [[0, 0, 1], [0, 0, -1], [0, 1, 0], [0, -1, 0], [-1, 0, 0], [1, 0, 0]],
            dtype=float,
        )
        self.update()

    def update(self):
        self.face_pos = self.pos + self.normals * CUBE_WIDTH / 2
        base = np.full((2, 2, 2, 3), CUBE_WIDTH / 2)
        base[..., 0, 0] *= -1
        base[:, 1, :, 1] *= -1
        base[1, ..., 2] *= -1
        self.vertices = base + self.pos
