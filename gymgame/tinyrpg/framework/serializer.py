from gymgame import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):

    def deserialize_action(self, data):
        return (config.Action.idle)


    def _gen_normalized_data(self, v):
        return v


    def _select(self, k):
        k.enter('map')

        k.enter('players')
        k.adds(self._select_character)
        k.exit()

        k.enter('npcs')
        k.adds(self._select_character)
        k.exit()

        k.exit()


    def _select_character(self, k):
        k.add(Attr.hp, None, k.n_division)
        k.add(Attr.max_hp, None, k.n_division)
        k.add(Attr.mp, None, k.n_division)
        k.add(Attr.max_mp, None, k.n_division)


    def _select_object(selfself, k):
        k.add(Attr.position, None, k.n_division)
        k.add(Attr.speed, None, k.n_division)
        k.add(Attr.radius, None, k.n_division)