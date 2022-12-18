"""
Functions that return 3-dimensional rotation arrays around some axis with a given angle.
"""
import numpy as np

_ROTATION_BUFFER = np.zeros((3, 3), dtype=float)

def x(theta):
    """
    Rotation around x-axis.
    """
    cos = np.cos(theta)
    sin = np.sin(theta)

    _ROTATION_BUFFER[:] = (
        (1,    0,   0),
        (0,  cos, sin),
        (0, -sin, cos),
    )

    return _ROTATION_BUFFER

def y(theta):
    """
    Rotation around y-axis.
    """
    cos = np.cos(theta)
    sin = np.sin(theta)

    _ROTATION_BUFFER[:] = (
        (cos, 0, -sin),
        (  0, 1,    0),
        (sin, 0,  cos),
    )

    return _ROTATION_BUFFER

def z(theta):
    """
    Rotation around z-axis.
    """
    cos = np.cos(theta)
    sin = np.sin(theta)

    _ROTATION_BUFFER[:] = (
        ( cos, sin, 0),
        (-sin, cos, 0),
        (   0,   0, 1),
    )

    return _ROTATION_BUFFER
