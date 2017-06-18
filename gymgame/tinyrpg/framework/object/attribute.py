import numpy as np


class Attribute(object):
    def __init__(self, name, init_required=False, base=None, range=None):
        self._name = name
        self._init_required = init_required
        self._base = base
        self._range = range
        self._plus_dict = {}
        self._base = self._clip(self._base)


    def __str__(self): return self.__repr__()

    def __repr__(self): return "{0}: {1}".format(self._name, self.value)

    @property
    def name(self): return self._name

    @property
    def init_required(self): return self._init_required

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, v):
        self._base = v

    @property
    def range(self):
        return self._range

    @property
    def value(self):
        sum = self._base
        for id, v in self._plus_dict.items():
            sum += v
        return self._clip(sum)


    def add_plus(self, id, value): self._plus_dict[id] = value


    def del_plus(self, id): return self._plus_dict.pop(id, None)


    def _clip(self, v):
        if self._range is None: return v
        min, max = self._range
        if min is not None and v < min: return min
        if max is not None and v > max: return max
        return v



class AttributeManager(object):
    def __init__(self):
        object.__setattr__(self, '_attr_dict', {})


    def __getattr__(self, id): return self.get(id).value


    def __setattr__(self, id, value): self.set_base_value(id, value)


    @property
    def init_required_attrs(self): return [name for name, attr in self._attr_dict.items() if attr.init_required]

    @property
    def attrs(self): return self._attr_dict.keys()


    def set_base_value(self, id, value): self.get(id).base = value


    def add_plus(self, id, pid, value): self.get(id).add_plus(pid, value)


    def del_plus(self, id, pid): self.get(id).del_plus(pid)


    def add(self, id, *args, **kwargs):
        if self.get(id, False) is not None: raise Exception("attribute {0} has been existed".format(id))
        attr = Attribute(id, *args, **kwargs)
        self._attr_dict[id] = attr


    def get(self, id, exception=True):
        attr = self._attr_dict.get(id, None)
        if attr is None and exception: raise Exception("attribute {0} is not existed".format(id))
        return attr




if __name__ == "__main__":
    attr = AttributeManager()
    attr.add('hp', 100)
    attr.hp += 1
    print(type(attr.hp), attr.hp)


