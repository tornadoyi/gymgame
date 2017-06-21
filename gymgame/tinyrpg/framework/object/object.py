from gymgame.engine import Event, Vector2
from ..config import Attr
from .attribute import AttributeManager
import numpy as np

# events:
#   on_update(object)

class Object(Event):
    def __init__(self, data):
        super(Object, self).__init__()
        self._attribute = AttributeManager()

        # init attribute
        self._init_attribute()

        # apply attrs
        self._apply_attribute(data)


        # runtime
        self._map = None

    def __getattr__(self, attr_name): return getattr(self._attribute, attr_name)


    @property
    def attribute(self): return self._attribute

    # events
    def update(self):
        self._update()
        self.send_event('on_update', self)

    def _update(self): pass



    def enter_map(self, map):
        assert self._map is None
        self._map = map

    def exit_map(self):
        assert self._map is not None
        self._map = None


    def idle(self): pass

    def move_toward(self, direct, speed=None): self._map.move_toward(self.attribute.id, direct)

    def move_to(self, position): self._map.move_to(self.attribute.id, position)


    def _init_attribute(self):
        attr = self._attribute
        attr.add(Attr.id, init_required=True)
        attr.add(Attr.position, base=Vector2(0, 0))
        attr.add(Attr.direct, base=Vector2(0, 0))
        attr.add(Attr.speed, base=0.0, range=(0, np.inf))
        attr.add(Attr.radius, base=0.0, range=(0, np.inf))



    def _apply_attribute(self, data):
        for k, v in data.items():
            self._attribute.set_base_value(k, v)

        data_attrs = data.keys()
        init_required_attrs = self._attribute.init_required_attrs
        for attr in init_required_attrs:
            if attr not in data_attrs: raise Exception('attribute {0} is init required'.format(attr))