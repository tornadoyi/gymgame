from .vector import *

class Line(object):
    def __init__(self, p0, p1):
        self._points = [p0, p1]


    @property
    def points(self): return self._points

    @property
    def start(self): return self._points[0]

    @property
    def end(self): return self._points[1]



class Line2(Line):

    @property
    def coefficients(self):
        # F(x) = ax + by + c = 0
        a = self.start.y - self.end.y
        b = self.end.x - self.start.x
        c = self.start.x * self.end.y - self.end.x * self.start.x
        return np.array([a, b, c])


    def cross(self, line):
        v = self.end - self.start
        v0 = line.start - self.start
        v1 = line.end - self.end
        s0 = v.x * v0.y - v.y * v0.x
        s1 = v.x * v1.y - v.y * v1.x
        return s0 * s1 <= 0


    def cross_point(self, line):
        if not self.cross(line): return None

        a0, b0, c0 = self.coefficients
        a1, b1, c1 = line.coefficients
        D = a0 * b1 - a1 * b0

        # same line
        if D == 0: return self.start

        # cross point
        x = (b0 * c1 - b1 * c0) / D
        y = (a1 * c0 - a0 * c1) / D
        return Vector2(x, y)


