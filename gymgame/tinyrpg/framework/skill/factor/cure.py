from . import factor


class Cure(factor.Factor):

    def __init__(self, value, relation):
        super(Cure, self).__init__(relation)
        self._value = value


    def __call__(self, src, dst, *args, **kwargs):
        dst.attribute.hp += self._value