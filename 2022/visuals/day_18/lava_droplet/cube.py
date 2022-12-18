import numpy as np

CUBE_WIDTH = .9


class Cube:
    __slots__ = "pos", "face_pos", "vertices", "normals"

    faces = (
                        #  Normal  #  # Swapped  #
        (           0, (0, 0, 1, 1), (0, 1, 1, 0)),  # Front
        (           1, (0, 0, 1, 1), (0, 1, 1, 0)),  # Back
            # Swapped  #                #  Normal  #
        ((0, 1, 1, 0),            0, (0, 0, 1, 1)),  # Top
        ((0, 1, 1, 0),            1, (0, 0, 1, 1)),  # Bottom
            #  Normal  #  # Swapped  #
        ((0, 0, 1, 1), (0, 1, 1, 0),            0),  # Left
        ((0, 0, 1, 1), (0, 1, 1, 0),            1),  # Right
    )

    def __init__(self, pos):
        self.pos = np.array(pos, dtype=float)

        self.normals = np.array(
            [
                [ 0,  0,  1], # Front
                [ 0,  0, -1], # Back
                [ 0,  1,  0], # Top
                [ 0, -1,  0], # Bottom
                [-1,  0,  0], # Left
                [ 1,  0 , 0], # Right
            ],
            dtype=float,
        )
        self.face_pos = self.pos + self.normals * CUBE_WIDTH / 2

        base = np.full((2, 2, 2, 3), CUBE_WIDTH / 2)
        base[..., 0, 0]  *= -1
        base[:, 1, :, 1] *= -1
        base[1, ..., 2]  *= -1
        self.vertices = base + pos

    def __matmul__(self, r):
        np.matmul(self.pos, r, out=self.pos)
        np.matmul(self.face_pos, r, out=self.face_pos)
        np.matmul(self.vertices, r, out=self.vertices)
        np.matmul(self.normals, r, out=self.normals)
