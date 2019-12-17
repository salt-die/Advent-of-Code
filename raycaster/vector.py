class Vec(tuple):
    def __add__(self, other):
        (x1, y1), (x2, y2) = self, other
        return Vec((x1 + x2, y1 + y2))

    def __sub__(self, other):
        (x1, y1), (x2, y2) = self, other
        return Vec((x1 - x2, y1 - y2))

    def __neg__(self):
        return Vec((-self[0], -self[1]))