"""
Script to generate the image for the ocean floor.
"""
import cv2
import numpy as np

from nurses_2.colors import AColor

from .depths import DEPTHS

SCALE = 10
FLOOR_COLOR = AColor.from_hex("050423ff")

def create_floor_texture():
    min_depth = min(DEPTHS)
    height = max(DEPTHS) - min_depth
    width = len(DEPTHS) * SCALE

    texture = np.zeros((height, width, 4), dtype=np.uint8)
    points = np.array([[SCALE * i, depth - min_depth] for i, depth in enumerate(DEPTHS)] + [[0, height]])
    cv2.fillPoly(texture, [points], FLOOR_COLOR)

    return texture
