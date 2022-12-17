from enum import IntFlag

import numpy as np

from .wall_kicks import *


class Orientation(IntFlag):
    """
    Orientation of a tetromino.
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def rotate(self, clockwise=True):
        return Orientation((self + (1 if clockwise else -1)) % 4)


class Tetromino:
    def __init_subclass__(cls):
        base = np.array(cls.BASE_SHAPE, dtype=np.uint8)

        cls.shapes = {
            Orientation.UP:    base,
            Orientation.RIGHT: np.rot90(base, 3),
            Orientation.DOWN:  np.rot90(base, 2),
            Orientation.LEFT:  np.rot90(base, 1),
        }

        cls.mino_positions = {
            orientation: np.argwhere(shape)
            for orientation, shape in cls.shapes.items()
        }

        cls.canvases = {
            orientation: np.where(shape, "@", " ")
            for orientation, shape in cls.shapes.items()
        }


class _(Tetromino):
    WALL_KICKS = I_WALL_KICKS
    BASE_SHAPE = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

class t(Tetromino):
    WALL_KICKS = O_WALL_KICKS
    BASE_SHAPE = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]

class J(Tetromino):
    WALL_KICKS = J_WALL_KICKS
    BASE_SHAPE = [
        [0, 0, 1],
        [0, 0, 1],
        [1, 1, 1],
    ]

class I(Tetromino):
    WALL_KICKS = I_WALL_KICKS
    BASE_SHAPE = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
    ]


class O(Tetromino):
    WALL_KICKS = O_WALL_KICKS
    BASE_SHAPE = [
        [1, 1],
        [1, 1],
    ]


TETROMINOS = _, t, J, I, O
