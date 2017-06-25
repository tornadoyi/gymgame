import numpy as np
from .object import Object
from ..config import Attr, is_enemy, is_friend, is_relation
from ..skill import SkillManager


class Character(Object):
    def __init__(self, data):
        super(Character, self).__init__(data)

        # init skill system
        self._skill = SkillManager(self, data.get('skills', []))


    @property
    def skill(self): return self._skill


    def cast_skill(self, skillid, target=None, position=None): self._skill.cast(skillid, target, position)


    def is_friend(self, o): return is_friend(self.attribute.camp , o.attribute.camp)


    def is_enemy(self, o): return is_enemy(self.attribute.camp , o.attribute.camp)


    def is_relation(self, relation, o): return is_relation(relation, self.attribute.camp , o.attribute.camp)


    def move_toward(self, direct, speed=None):
        if not self.can_move(): return
        self._map.move_toward(self.attribute.id, direct, speed)


    def move_to(self, position):
        if not self.can_move(): return
        self._map.move_to(self.attribute.id, position)


    def can_move(self): return not self._skill.busy


    def _update(self):
        self._skill.update()


    def _init_attribute(self):
        super(Character, self)._init_attribute()

        self._add_attr('static', Attr.camp, base=0)
        self._add_attr('plus', Attr.max_hp, base=0.0, range=(0, np.inf))
        self._add_attr('plus', Attr.max_mp, base=0.0, range=(0, np.inf))
        self._add_attr('value', Attr.hp, base=self._attribute.max_hp, range=(0, lambda: self._attribute.max_hp))
        self._add_attr('value', Attr.mp, base=self._attribute.max_mp, range=(0, lambda: self._attribute.max_mp))






class NPC(Character):
    pass


class Player(Character):
    pass