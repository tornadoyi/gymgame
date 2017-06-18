from .object import Object
from ..config import Attr
import numpy as np

class Character(Object):
    def __init__(self, attribute):
        super(Character, self).__init__(attribute)


    def do_skill(self, skillid, target=None, area=None): raise NotImplementedError("todo !!,  need to be implemented")


    def _init_attribute(self):
        super(Character, self)._init_attribute()

        attr = self._attribute
        attr.add(Attr.hp, base=0.0, range=(0, np.inf))
        attr.add(Attr.max_hp, base=0.0, range=(0, np.inf))
        attr.add(Attr.mp, base=0.0, range=(0, np.inf))
        attr.add(Attr.max_mp, base=0.0, range=(0, np.inf))



class NPC(Character):
    pass


class Player(Character):
    pass