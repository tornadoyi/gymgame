import numpy as np
from .. import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):
    
    def __init__(self, grid_size=None):
        self._grid_size = grid_size
        super(Serializer, self).__init__()


    def serialize_state(self, game):
        return self._serialize_to_grid(game, self._grid_size or game.map.bounds.size)


    def _serialize_to_grid(self, game, grid_size):
        map = game.map
        scale = grid_size / map.bounds.size
        coins = map.coins
        bullets = map.bullets
        players = map.players

        grid_min, grid_max = np.zeros(2, dtype=int), (grid_size-1).astype(int)

        def _objs_to_grid(objs, path):
            num = len(objs)
            s = self._kernel.serialize_node(objs, path, self._norm)
            s_mat = s.reshape((num, -1))
            c = s_mat.shape[-1]
            grid = np.zeros((int(grid_size[0]), int(grid_size[1]), c), dtype=np.float64)

            for i in range(len(objs)):
                o = objs[i]
                position = o.attribute.position * scale
                r = o.attribute.radius * scale
                min, max = np.round(position-r).astype(int), np.round(position+r).astype(int) + 1
                min, max = np.max([grid_min, min], axis=0), np.min([grid_max, max], axis=0)
                grid[min[0]:max[0], min[1]:max[1]] = s_mat[i]

            return grid

        player_grid = _objs_to_grid(players, '/map/players')
        coin_gird = _objs_to_grid(players, '/map/coins')
        bullet_grid = _objs_to_grid(players, '/map/bullets')

        grid = np.concatenate((player_grid, coin_gird, bullet_grid), axis=2)
        return grid









    def _deserialize_action(self, data): return []


    def _select(self, k, *args):
        k.enter('map')

        k.enter('players')
        self._select_character(k)
        k.exit()

        k.enter('coins')
        self._select_character(k)
        k.exit()

        k.enter('bullets')
        self._select_character(k)
        k.exit()

        k.exit()

    def _select_character(self, k):
        self._select_object(k)
        k.add(Attr.hp, None, k.n_div_tag(Attr.hp))



