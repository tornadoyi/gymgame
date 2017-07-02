import numpy as np
from .. import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):
    
    def __init__(self, grid_size=None):
        self._grid_size = grid_size
        super(Serializer, self).__init__()


    @property
    def coin_shape(self): return self._coin_shape


    def _start(self, game):
        super(Serializer, self)._start(game)
        k = self._create_kernel(game)

        map = game.map
        self._coin_shape = k.do_object(map.coins[0], self._serialize_npc).shape



    def _deserialize_action(self, data): return []


    def _serialize_map(self, k, map):
        s_players = k.do_object(map.players, self._serialize_player)
        s_coins = k.do_object(map.coins, self._serialize_npc)
        s_bullets = k.do_object(map.bullets, self._serialize_npc)

        if self._grid_size is None:
            return np.hstack([s_players, s_coins, s_bullets])

        else:
            bounds = map.bounds
            grid_players = self._objects_to_grid(bounds, map.players, s_players, self._player_shape)
            grid_coins = self._objects_to_grid(bounds, map.coins, s_coins, self._coin_shape)
            grid_bullets = self._objects_to_grid(bounds, map.bullets, s_bullets, self._bullet_shape)
            return np.concatenate([grid_players, grid_coins, grid_bullets], axis=2)


    def _serialize_character(self, k, char):
        attr = char.attribute
        k.do(attr.hp, None, k.n_div_tag, Attr.hp)



