

class Bounds(object):
    def __init__(self, center, size):
        self._center = center
        self._size = size


    @property
    def center(self): return self._center

    @center.setter
    def center(self, v): self._center = v


    @property
    def size(self): return self._size

    @size.setter
    def size(self, v): self._size = v


    @property
    def min(self): return self.center - (self.size-1) / 2

    @property
    def max(self): return self.center + (self.size-1) / 2



class Bounds2(Bounds):
    pass



class Bounds3(Bounds):
    pass