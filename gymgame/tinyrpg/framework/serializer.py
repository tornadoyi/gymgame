import numpy as np
from gymgame import framework
from . import config


Attr = config.Attr

class Serializer(framework.Serializer):


    def _select(self, k, *args):
        k.enter('map')

        k.enter('players')
        self._select_character(k)
        k.exit()

        k.enter('npcs')
        self._select_character(k)
        k.exit()

        '''
        k.enter('bullets')
        self._select_bullet(k)
        k.exit()
        '''

        k.exit()


    def _select_character(self, k):
        self._select_object(k)
        k.add(Attr.hp, None, k.n_div_tag(Attr.hp))
        k.add(Attr.max_hp, None, k.n_div_tag(Attr.max_hp))
        k.add(Attr.mp, None, k.n_div_tag(Attr.mp))
        k.add(Attr.max_mp, None, k.n_div_tag(Attr.max_mp))


    def _select_object(self, k):
        k.add(Attr.position, None, lambda v, norm: v / norm.game.map.bounds.size * 2)
        k.add(Attr.direct, None, k.n_none())
        k.add(Attr.speed, None, k.n_div_tag(Attr.speed))
        k.add(Attr.radius, None, k.n_div_tag(Attr.radius))


    def _select_bullet(self, k):
        k.add(Attr.hp, None, k.n_div_tag(Attr.hp))
        k.add(Attr.max_hp, None, k.n_div_tag(Attr.max_hp))

