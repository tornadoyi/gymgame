import copy
from easydict import EasyDict as edict
import numpy as np
from ..framework import data
from .config import *


class Data(data.Data):

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



    def _create_npc_infos(self):
        npcs = []
        for i in range(NUM_NPC):
            npc = copy.deepcopy(BASE_NPC)
            npc.id = npc.id.format(i)
            npc.position = gen_init_position(self.map_center, NPC_INIT_RADIUS)
            npcs.append(npc)
        return npcs





