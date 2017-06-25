from gymgame.engine import  Vector2, Scheduler
from ..config import Attr
from .attribute import Attribute, PlusAttribute, AttributeManager
import numpy as np

# events:
#   on_update(object)

class Object(Scheduler):
    def __init__(self, data):
        super(Object, self).__init__()
        self._data = data
        self._attribute = AttributeManager()

        # init attribute
        self._init_attribute()

        # runtime
        self._map = None
        self._game = None


    def __getattr__(self, attr_name): return getattr(self._attribute, attr_name)


    @property
    def attribute(self): return self._attribute

    @property
    def map(self): return self._map

    @property
    def game(self): return self._game


    # events
    def update(self):
        super(Object, self).update(self._game.time)


    def _update(self): pass



    def enter_map(self, map):
        assert self._map is None
        self._map = map
        self._game = map.game

    def exit_map(self):
        assert self._map is not None
        self._map = None
        self._game = None


    def idle(self): pass

    def move_toward(self, direct, speed=None): self._map.move_toward(self.attribute.id, direct, speed)

    def move_to(self, position): self._map.move_to(self.attribute.id, position)


    def _init_attribute(self):

        self._add_attr('static', Attr.id)
        self._add_attr('value', Attr.position, base=Vector2(0, 0))
        self._add_attr('value', Attr.direct, base=Vector2(0, 0))
        self._add_attr('value', Attr.radius, base=0.0,   range=(0, np.inf))
        self._add_attr('plus', Attr.speed, base=0.0,   range=(0, np.inf))


    def _add_attr(self, type, name, base=None, *args, **kwargs):
        init_value = self._data.get(name, None)
        if init_value is None: init_value = base
        if init_value is None: raise Exception('attribute {0} of {1} is required'.format(name, type(self)))
        self._attribute.add(type, name, init_value, *args, **kwargs)


