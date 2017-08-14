import numpy as np
from .. import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):
    
    def __init__(self, *args, **kwargs):
        super(Serializer, self).__init__(*args, **kwargs)


    @property
    def coin_shape(self): return self._coin_shape


    def _start(self, game):
        k = self._create_kernel(game)
        map = game.map

        self._player_shape = k.do_object(map.players[0], self._serialize_player).shape if len(map.players) > 0 else None
        self._coin_shape = k.do_object(map.coins[0], self._serialize_npc).shape if len(map.coins) > 0 else None
        self._bullet_shape = k.do_object(map.bullets[0], self._serialize_npc).shape if len(map.bullets) > 0 else None

        # call parent _start
        super(framework.Serializer, self)._start(game)




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

            assemble = []
            if grid_players is not None: assemble.append(grid_players)
            if grid_coins is not None: assemble.append(grid_coins)
            if grid_bullets is not None: assemble.append(grid_bullets)

            return np.concatenate(assemble, axis=2)


    def _serialize_coin(self, k, coin): self._serialize_character(k, coin)

    def _serialize_bullet(self, k, bullet): self._serialize_character(k, bullet)

    def _serialize_character(self, k, char):
        if self._grid_size is None:
            self._serialize_character_flat(k, char)
        else:
            self._serialize_character_grid(k, char)


    def _serialize_character_flat(self, k, char):
        attr = char.attribute
        k.do(attr.hp, None, k.n_div_tag, Attr.hp)
        k.do(attr.position, None, lambda v, norm: v / norm.game.map.bounds.max)


    def _serialize_character_grid(self, k, char):
        attr = char.attribute
        k.do(attr.hp, None, k.n_div_tag, Attr.hp)


