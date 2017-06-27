import types
import numpy as np

class Attribute(object):
    def __init__(self, name, base):
        self._name = name
        self._base = base

    def __str__(self): return self.__repr__()

    def __repr__(self): return "{0}: {1}".format(self._name, self.value)

    @property
    def name(self): return self._name

    @property
    def value(self): return self._base

    @value.setter
    def value(self, v): self._base = v



class StaticAttribute(Attribute):
    @property
    def value(self): return self._base


    @value.setter
    def value(self, v): raise Exception('{0} can not set value'.format(type(self)))



class ValueAttribute(Attribute):
    def __init__(self, name, base, range=None):
        super(ValueAttribute, self).__init__(name, base)
        self._range = range
        self._base = self._clip(self._base)


    @property
    def value(self): return self._base


    @value.setter
    def value(self, v): self._base = self._clip(v)


    def _clip(self, v):
        if self._range is None: return v
        min, max = self._range
        min = min() if isinstance(min, (types.FunctionType, types.MethodType)) else min
        max = max() if isinstance(max, (types.FunctionType, types.MethodType)) else max
        if min is not None and v < min: return min
        if max is not None and v > max: return max
        return v



class PlusAttribute(ValueAttribute):
    def __init__(self, *args, **kwargs):
        super(PlusAttribute, self).__init__(*args, **kwargs)
        self._plus_dict = {}
        self._value = self._base
        self._dirty = False


    @property
    def value(self):
        if not self._dirty: return self._value
        sum = self._base
        for name, v in self._plus_dict.items(): sum += v
        self._value = self._clip(sum)
        self._dirty = False
        return self._value


    @value.setter
    def value(self, v): raise Exception('{0} can not set value directly'.format(type(self)))


    def add_plus(self, name, value):
        self._plus_dict[name] = value
        self._dirty = True

    def del_plus(self, name):
        plus = self._plus_dict.pop(name, None)
        if plus is None: return None
        self._dirty = True




class AttributeManager(object):
    def __init__(self):
        object.__setattr__(self, '_attr_dict', {})


    def __getattr__(self, name): return self.get_value(name)


    def __setattr__(self, name, value): self.set_value(name, value)


    @property
    def attrs(self): return self._attr_dict.keys()


    def set_value(self, name, value): self.get(name).value = value


    def get_value(self, name): return self.get(name).value


    def add_plus(self, name, pname, value): self.get(name).add_plus(pname, value)


    def del_plus(self, name, pname): self.get(name).del_plus(pname)


    def add(self, type, name, *args, **kwargs):
        if self.get(name, False) is not None: raise Exception("attribute {0} has been existed".format(name))

        if type == 'static': attr = StaticAttribute(name, *args, **kwargs)
        elif type == 'value': attr = ValueAttribute(name, *args, **kwargs)
        elif type == 'plus': attr = PlusAttribute(name, *args, **kwargs)
        else: raise Exception('invalid attribute type {0}'.format(type))

        self._attr_dict[name] = attr


    def get(self, name, exception=True):
        attr = self._attr_dict.get(name, None)
        if attr is None and exception: raise Exception("attribute {0} is not existed".format(name))
        return attr





