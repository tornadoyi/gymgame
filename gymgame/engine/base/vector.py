import math
import numpy as np

_dtype = float


class Vector(np.ndarray):
    @staticmethod
    def __new__(cls, arr, dtype=_dtype): return np.ndarray.__new__(cls, shape=(len(arr), ), buffer=np.array(arr, dtype=dtype), dtype=dtype)

    @property
    def sqr_magnitude(self): return np.sum(self ** 2)

    @property
    def magnitude(self): return np.sqrt(self.sqr_magnitude)

    @property
    def normalized(self):
        if np.all(self == 0):
            return self
        else:
            return self / self.magnitude


    def redian(self, v): return np.arccos(self.dot(v) / (self.magnitude * v.magnitude))

    def angle(self, v): return self.redian(v) * 180 / np.pi

    def dot(self, *args): return super(Vector, self).dot(*args)

    def distance(self, v): return (v - self).magnitude



class Vector2(Vector):
    down = None
    left = None
    one = None
    right = None
    up = None
    zero = None

    @staticmethod
    def __new__(cls, x, y, *args): return Vector.__new__(cls, [x, y], *args)


    @property
    def x(self): return self[0]

    @property
    def y(self): return self[1]

    def rotate(self, angle):
        r = math.radians(angle)
        x, y = self.x, self.y
        return Vector2(np.cos(r) * x - np.sin(r) * y, np.sin(r) * x + np.cos(r) * y)



Vector2.down = Vector2(0, -1)
Vector2.left = Vector2(-1, 0)
Vector2.one = Vector2(1, 1)
Vector2.right = Vector2(1, 0)
Vector2.up = Vector2(0, 1)
Vector2.zero = Vector2(0, 0)


class Vector3(Vector):
    back = None
    down = None
    forward = None
    left = None
    one = None
    right = None
    up = None
    zero = None


    @staticmethod
    def __new__(cls, x, y, z, *args): return Vector.__new__(cls, [x, y, z], *args)

    @property
    def x(self): return self[0]

    @property
    def y(self): return self[1]

    @property
    def z(self): return self[2]



Vector3.back = Vector3(0, 0, -1)
Vector3.down = Vector3(0, -1, 0)
Vector3.forward = Vector3(0, 0, 1)
Vector3.left = Vector3(-1, 0, 0)
Vector3.one = Vector3(1, 1, 1)
Vector3.right = Vector3(1, 0, 0)
Vector3.up = Vector3(0, 1, 0)
Vector3.zero = Vector3(0, 0, 0)

