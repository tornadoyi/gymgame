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
                min, max = np.floor(position-r).astype(int), np.ceil(position+r).astype(int)
                min, max = np.max([grid_min, min], axis=0), np.min([grid_max, max], axis=0)
                grid[min[0]:max[0], min[1]:max[1]] = s_mat[i]

            return grid


        grid_list = []

        grid_list.append(_objs_to_grid(players, '/map/players'))

        if config.NUM_COIN > 0: grid_list.append(_objs_to_grid(coins, '/map/coins'))

        if config.NUM_BULLET > 0: grid_list.append(_objs_to_grid(bullets, '/map/bullets'))

        grid = np.concatenate(grid_list, axis=2)
        return grid



    def _deserialize_action(self, data): return []


    def _select(self, k, *args):
        k.enter('map')

        k.enter('players')
        self._select_character(k)
        k.exit()

        if config.NUM_COIN:
            k.enter('coins')
            self._select_character(k)
            k.exit()


        if config.NUM_BULLET:
            k.enter('bullets')
            self._select_character(k)
            k.exit()

        k.exit()

    def _select_character(self, k):
        k.add(Attr.hp, None, k.n_div_tag(Attr.hp))



