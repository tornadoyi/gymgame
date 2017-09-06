import numpy as np

class Bounds(object):
    def __init__(self, center, size):
        self._center = center
        self._size = size

    def __str__(self): return '({} {})'.format(self._center, self._size)

    def __repr__(self): return self.__str__()

    @property
    def center(self): return self._center

    @center.setter
    def center(self, v): self._center = v


    @property
    def size(self): return self._size

    @size.setter
    def size(self, v): self._size = v


    @property
    def min(self): return self.center - self.size / 2

    @property
    def max(self): return self.center + self.size / 2


    def contains(self, v):
        min, max = self.min, self.max
        if v.x < min.x or v.x > max.x: return False
        if v.y < min.y or v.y > max.y: return False
        return True

    def intersects(self, b):
        minx = np.max([self.min.x, b.min.x])
        maxx = np.min([self.max.x, b.max.x])
        miny = np.max([self.min.y, b.min.y])
        maxy = np.min([self.max.y, b.max.y])
        return minx <= maxx and miny <= maxy




class Bounds2(Bounds):
    pass



class Bounds3(Bounds):
    pass