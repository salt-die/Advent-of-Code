from computer import Computer
import cv2
import numpy as np
import matplotlib.pyplot as plt
from stitch import stitch

class Arcade:
    def __init__(self, animate=''):
        self.animate = animate
        if animate:
            self.counter = 0

    def load(self, data):
        self.processor = Computer(int_code=data)

    __lshift__ = load

    def show(self, animate=False):
        xs = [x for x, _ in self.pixels]
        ys = [y for _, y in self.pixels]

        min_xy = min(xs), min(ys)
        width = np.ptp(xs) + 1
        height = np.ptp(ys) + 1

        self.screen = np.zeros([width, height])
        for location, pixel in self.pixels.items():
            location = tuple(np.array(location) - min_xy)
            self.screen[location] = pixel

        if animate:
            self.counter += 1
            if self.counter < 300:
                cv2.imwrite(f'frames/{self.counter:03d}.png',
                            cv2.resize(self.screen * 62, (350, 250),
                                       interpolation=cv2.INTER_NEAREST))
        else:
            plt.imshow(self.screen)
            plt.show()

    def start(self, quarters=None):
        self.pixels = {}
        if quarters is not None:
            self.processor.int_code[0] = 2

        for _, op, _, _, _ in self.processor:
            if len(self.processor) == 3:
                z, y, x = self.processor.out
                self.processor.out.clear()
                if x == -1 and y == 0:
                    self.score = z
                else:
                    if z == 4:
                        ball_pos = x
                    elif z == 3:
                        paddle_pos = x
                    self.pixels[(y, x)] = z

            if op == '03':
                if self.animate:
                    self.show(animate=True)
                self.processor << np.sign(ball_pos - paddle_pos)

        if self.animate:
            stitch(self.animate, .01)
