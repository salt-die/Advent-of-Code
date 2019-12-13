from computer import Computer
from display import Display, array_from_dict
import numpy as np

class Arcade:
    def load(self, data):
        self.processor = Computer(int_code=data)

    __lshift__ = load

    def show(self):
        if isinstance(self.pixels, dict):
            self.pixels = array_from_dict(self.pixels)

        self.display(self.pixels, Score=self.score)

    def start(self, quarters=None):
        self.pixels = {}

        if quarters is not None:
            self.processor.int_code[0] = 2

        self.run_game()

    __call__ = start

    def run_game(self):
        self.score = 0
        self.display = Display()
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
                    self.pixels[y, x] = z

            if op == '03':
                self.show()
                self.processor << np.sign(ball_pos - paddle_pos)

        self.show()
        self.display.text('GAME OVER')
        self.display.stop()