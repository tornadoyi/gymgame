import numpy as np
from gymgame import framework
from .object import Bullet
from . import config


Attr = config.Attr

class Serializer(framework.Serializer):
    def __init__(self, grid_size = None, *args, **kwargs):
        super(Serializer, self).__init__(*args, **kwargs)
        self._grid_size = None if grid_size is None else np.array(grid_size, dtype=int)



    @property
    def grid_size(self): return self._grid_size


    def _start(self, game):
        # get all object shape
        k = self._create_kernel()
        map = game.map

        self._player_shape = k.do_object(map.players[0], self._serialize_player).shape if len(map.players) > 0 else None
        self._npc_shape = k.do_object(map.npcs[0], self._serialize_npc).shape if len(map.npcs) > 0 else None
        self._bullet_shape = k.do_object(Bullet({'id': 'sample'}), self._serialize_bullet).shape

        # call parent _start
        super(Serializer, self)._start(game)



    @property
    def player_shape(self): return self._player_shape


    @property
    def npc_shape(self): return self._npc_shape


    @property
    def bullet_shape(self): return self._bullet_shape


    def _serialize_state(self, k, game): return self._serialize_map(k, game.map)


    def _serialize_map(self, k, map):
        s_players = k.do_object(map.players, self._serialize_player)
        s_npcs = k.do_object(map.npcs, self._serialize_npc)
        s_bullets = k.do_object(map.bullets, self._serialize_bullet)

        if self._grid_size is None:
            return np.hstack([s_players, s_npcs, s_bullets])

        else:
            bounds = map.bounds
            grid_players = self._objects_to_grid(bounds, map.players, s_players, self._player_shape)
            grid_npcs = self._objects_to_grid(bounds, map.npcs, s_npcs, self._npc_shape)
            grid_bullets = self._objects_to_grid(bounds, map.bullets, s_bullets, self._bullet_shape)

            assemble = []
            if grid_players is not None: assemble.append(grid_players)
            if grid_npcs is not None: assemble.append(grid_npcs)
            if grid_bullets is not None: assemble.append(grid_bullets)

            return np.concatenate(assemble, axis=2)


    def _serialize_player(self, k, player): self._serialize_character(k, player)


    def _serialize_npc(self, k, npc): self._serialize_character(k, npc)


    def _serialize_bullet(self, k, bullet):
        self._serialize_object(k, bullet)
        attr = bullet.attribute
        k.do(attr.hp, None, k.n_div_tag, Attr.hp)
        k.do(attr.max_hp, None, k.n_div_tag, Attr.max_hp)


    def _serialize_character(self, k, char):
        self._serialize_object(k, char)
        attr = char.attribute
        k.do(attr.hp, None, k.n_div_tag, Attr.hp)
        k.do(attr.max_hp, None, k.n_div_tag, Attr.max_hp)
        k.do(attr.mp, None, k.n_div_tag, Attr.mp)
        k.do(attr.max_mp, None, k.n_div_tag, Attr.max_mp)


    def _serialize_object(self, k, obj):
        attr = obj.attribute
        k.do(attr.position, None, lambda v, norm: v / norm.game.map.bounds.max)
        k.do(attr.direct, None, None)
        k.do(attr.speed, None, k.n_div_tag, Attr.speed)
        k.do(attr.radius, None, k.n_div_tag, Attr.radius)



    def _objects_to_grid(self, bounds, objs, sobjs, shape):
        if shape is None: return None
        offset = abs(bounds.min)
        scale = self._grid_size / bounds.size
        grid = np.zeros((int(self._grid_size[0]), int(self._grid_size[1]), shape[0]), dtype=self._dtype)
        if len(objs) == 0: return grid

        grid_min, grid_max = np.zeros(2, dtype=int), self._grid_size.astype(int)

        s_mat = sobjs.reshape((len(objs), -1))
        for i in range(len(objs)):
            o = objs[i]
            position = (o.attribute.position + offset) * scale
            r = o.attribute.radius * scale
            min, max = np.round(position - r).astype(int), np.round(position + r).astype(int)

            # occupy one cell as least
            sub = np.max([max - min, (1, 1)], axis=0)
            max = min + sub

            # check bounds
            if (min < grid_min).any() or (max > grid_max).any(): continue

            # ocuupy
            grid[min[0]:max[0], min[1]:max[1]] += s_mat[i]

        return grid




