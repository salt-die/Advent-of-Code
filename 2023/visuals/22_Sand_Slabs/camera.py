import cv2
import numpy as np
from numpy.linalg import norm

from . import rotation


class Camera:
    __slots__ = (
        "translation",
        "plane",
        "camera_matrix",
        # Buffers
        "_POINTS_2D_INT_BUFFER",
        "_NORMALS_BUFFER",
        "_POS_BUFFER",
    )

    INITIAL_Z_DISTANCE = 24.0

    INITIAL_X_ANGLE = np.pi / 2
    INITIAL_Y_ANGLE = -np.pi
    INITIAL_Z_ANGLE = 0

    CX = 0.0  # x-center of image
    CY = 0.0  # y-center of image
    FX = 1.0  # x-focal length
    FY = 1.0  # y-focal length

    DISTORTION_COEF = np.array([0.0, 0.0, 0.0, 0.0])

    def __init__(self):
        self._POINTS_2D_INT_BUFFER = np.zeros((2, 2, 2, 2), dtype=int)
        self._NORMALS_BUFFER = np.zeros(6, dtype=float)
        self._POS_BUFFER = np.zeros(3, dtype=float)

        self.translation = np.array([0.0, 0.0, self.INITIAL_Z_DISTANCE])

        self.plane = plane = rotation.x(self.INITIAL_X_ANGLE).copy()
        np.matmul(plane, rotation.y(self.INITIAL_Y_ANGLE), out=plane)
        np.matmul(plane, rotation.z(self.INITIAL_Z_ANGLE), out=plane)

        self.camera_matrix = np.array(
            [
                [self.FX, 0.0, self.CX],
                [0.0, self.FY, self.CY],
                [0.0, 0.0, 1.0],
            ]
        )

    @property
    def z_distance(self):
        return self.translation[-1]

    @z_distance.setter
    def z_distance(self, distance):
        self.translation[-1] = distance

    @property
    def pos(self):
        return -self.plane.T @ self.translation

    @property
    def focal_x(self):
        return self.camera_matrix[0, 0]

    @focal_x.setter
    def focal_x(self, value):
        self.camera_matrix[0, 0] = value

    @property
    def focal_y(self):
        return self.camera_matrix[1, 1]

    @focal_y.setter
    def focal_y(self, value):
        self.camera_matrix[1, 1] = value

    def rotate_x(self, theta):
        np.matmul(self.plane, rotation.x(theta), out=self.plane)

    def rotate_y(self, theta):
        np.matmul(self.plane, rotation.y(theta), out=self.plane)

    def rotate_z(self, theta):
        np.matmul(self.plane, rotation.z(theta), out=self.plane)

    def render_cube(self, cube, image, aspect_ratio=True):
        h, w, _ = image.shape

        if aspect_ratio:
            if w > h:
                self.focal_x = h / w
                self.focal_y = 1.0
            else:
                self.focal_x = 1.0
                self.focal_y = w / h

        points_2d, _ = cv2.projectPoints(
            cube.vertices.reshape(-1, 3),
            cv2.Rodrigues(self.plane)[0],
            self.translation,
            self.camera_matrix,
            self.DISTORTION_COEF,
        )

        # Translate to center and scale to image:
        points_2d += 0.5
        points_2d *= w, h

        vertices_2d = self._POINTS_2D_INT_BUFFER
        vertices_2d[:] = points_2d.reshape(2, 2, 2, 2)  # Cast to int

        pos = self.pos

        faces = [
            (norm(face_pos - pos), face)
            for face_pos, face in zip(cube.face_pos, cube.faces)
        ]

        # Sort faces by distance to camera.
        faces.sort(key=lambda tup: tup[0], reverse=True)
        r, g, b, a = cube.color

        for distance, face in faces:
            p = np.e ** -(distance * 0.02)
            cv2.fillConvexPoly(
                image, vertices_2d[face], (int(p * r), int(p * g), int(p * b), a)
            )
