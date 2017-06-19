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



class Line2(object):

    def cross(self, line):
        v = self.end - self.start
        v0 = line.start - self.start
        v1 = line.end - self.end
        s0 = v.x * v0.y - v.y * v0.x
        s1 = v.x * v1.y - v.y * v1.x
        return s0 * s1 <= 0

