import numpy as np
from gymgame import framework
from . import config


Attr = config.Attr

class Serializer(framework.Serializer):

    def deserialize_action(self, data):
        return (config.Action.idle)


    def _gen_normalized_data(self, v, game, *args):
        k = self._kernel
        map = game.map
        n_players = len(map.players)
        n_npcs = len(map.npcs)
        n_chars = n_players + n_npcs

        batch_v = v.reshape([n_chars, -1])
        max_v = np.max(batch_v, axis=0)

        pos_node = k.node('/map/players/0/position')
        if pos_node is not None:
            max_v[pos_node.start_pos : pos_node.end_pos] = [map.bounds.size.x, map.bounds.size.y]

        return np.tile(max_v, n_chars)



    def _select(self, k, *args):
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


    def _select_object(self, k):
        k.add(Attr.position, None, k.n_division)
        k.add(Attr.direct, None, k.n_division)
        k.add(Attr.speed, None, k.n_division)
        k.add(Attr.radius, None, k.n_division)


