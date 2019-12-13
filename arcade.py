from computer import Computer
import numpy as np
import matplotlib.pyplot as plt
#cv2.imwrite(f'frames/{next(self.counter):03d}.png',
#            cv2.resize(self.array, (430, 60), interpolation=cv2.INTER_NEAREST))
class Arcade:
    def load(self, data):
        self.processor = Computer(int_code=data)

    __lshift__ = load

    def show(self):
        xs = [x for x, _ in self.pixels]
        ys = [y for _, y in self.pixels]

        min_xy = min(xs), min(ys)
        width = np.ptp(xs) + 1
        height = np.ptp(ys) + 1

        self.screen = np.zeros([width, height])
        for location, pixel in self.pixels.items():
            location = tuple(np.array(location) - min_xy)
            self.screen[location] = pixel

        plt.imshow(self.screen)
        plt.show()

    def start(self, quarters=None):
        self.pixels = {}
        if quarters is not None:
            self.processor.int_code[0] = 2

        for _,op,_,_,_ in self.processor.compute_iter():
            if len(self.processor) == 3:
                z, y, x = self.processor.out
                self.processor.out.clear()
                if x == -1 and y == 0:
                    self.score = z
                else:
                    if z == 4:
                        ball_pos = x
                    if z == 3:
                        paddle_pos = x
                    self.pixels[(y, x)] = z

            if op == '03':
                self.processor << np.sign(ball_pos - paddle_pos)
