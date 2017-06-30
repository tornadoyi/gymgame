from easydict import EasyDict as edict
import numpy as np
from ..framework import data
from .config import *


class Data(data.Data):
    def __init__(self, map_cls=None, player_cls=None, bullet_cls=None, coin_cls=None):
        super(Data, self).__init__(map_cls, player_cls, None)
        self._bullet_cls = bullet_cls
        self._coin_cls = coin_cls


    @property
    def map_center(self): return (MAP_SIZE - 1) / 2

    def _create_map_info(self): return edict(size=MAP_SIZE)


    def _create_player_infos(self):
        players = []
        for i in range(NUM_PLAYERS):
            player = copy.deepcopy(BASE_PLAYER)
            player.id = player.id.format(i)
            player.position = gen_init_position(self.map_center, PLAYER_INIT_RADIUS)
            players.append(player)
        return players



    def _reset_npcs(self):
        self._npcs = []
        self._bullet_infos = copy.deepcopy(self._create_bullet_infos())
        for info in self._bullet_infos: self._npcs.append(self._bullet_cls(info))

        self._coin_infos = copy.deepcopy(self._create_coin_infos())
        for info in self._coin_infos: self._npcs.append(self._coin_cls(info))


    def _create_bullet_infos(self):
        bullets = []
        index = np.random.randint(0, len(self._player_infos))
        player = self._player_infos[index]

        for i in range(NUM_BULLET):
            # position and direct
            position = gen_init_position(self.map_center, BULLET_INIT_RADIUS)
            direct = gen_aim_direct(position, player.position)

            bullet = copy.deepcopy(BASE_BULLET)
            bullet.id = bullet.id.format(i)
            bullet.position = position
            bullet.direct = direct
            bullets.append(bullet)

        return bullets


    def _create_coin_infos(self):
        coins = []
        for i in range(NUM_COIN):
            coin = copy.deepcopy(BASE_COIN)
            coin.id = coin.id.format(i)
            coin.position = gen_init_position(self.map_center, COIN_INIT_RADIUS)
            coins.append(coin)
        return coins





