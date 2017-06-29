from easydict import EasyDict as edict
import numpy as np
from ..framework import data
from .config import *


class Data(data.Data):

    def _create_map_info(self): return edict(center=MAP_CENTER, size=MAP_SIZE)

    def _create_player_infos(self):
        players = []
        for i in range(NUM_PLAYERS):
            player = copy.deepcopy(BASE_PLAYER)
            player.id = player.id.format(i)
            # player.position = gen_init_position(PLAYER_INIT_RADIUS)
            players.append(player)
        return players



    def _create_npc_infos(self):
        npcs = []
        index = np.random.randint(0, len(self._player_infos))
        player = self._player_infos[index]

        for i in range(NUM_NPC):
            # position and direct
            position = self._gen_init_position(NPC_INIT_RADIUS)
            direct = self._gen_npc_direct(position, player.position)

            npc = copy.deepcopy(BASE_NPC)
            npc.id = npc.id.format(i)
            npc.position = position
            npc.direct = direct
            npcs.append(npc)

        return npcs

    def _gen_init_position(self, r_range):
        r_range = np.array(r_range)
        minx, maxx = MAP_SIZE.x / 2 * r_range
        miny, maxy = MAP_SIZE.y / 2 * r_range
        r = Vector2(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
        direct = Vector2(*np.random.uniform(-1.0, 1.0, 2))
        return direct.normalized * r


    def _gen_npc_direct(self, src_pos, dst_pos):
        def _aim():
            direct = dst_pos - src_pos
            angle = np.random.uniform(-NPC_DIRECT_SHAKE_ANGLE, NPC_DIRECT_SHAKE_ANGLE)
            return direct.rotate(angle)

        def _random():
            return Vector2(*np.random.uniform(-1, 1, 2))

        if np.random.rand() < NPC_AIM_PROBABILITY:
            return _aim()
        else:
            return _random()



