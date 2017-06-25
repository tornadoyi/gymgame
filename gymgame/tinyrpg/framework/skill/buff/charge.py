from . import factor


class Charge(factor.Factor):

    def __init__(self, value):
        self._value = value

    def __call__(self, src, dst, *args, **kwargs):
        dst.attribute.hp += self._value