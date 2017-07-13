import copy
from easydict import EasyDict as edict
import numpy as np
from ..framework import data
from . import config


class Data(data.Data):

    @property
    def map_center(self): return config.MAP_SIZE / 2

    def _create_map_info(self): return edict(size=config.MAP_SIZE)


    def _create_player_infos(self):
        players = []
        for i in range(config.NUM_PLAYERS):
            player = copy.deepcopy(config.BASE_PLAYER)
            player.id = player.id.format(i)
            player.position = config.gen_init_position(self.map_center, config.PLAYER_INIT_RADIUS)
            players.append(player)
        return players



    def _create_npc_infos(self):
        npcs = []
        for i in range(config.NUM_NPC):
            npc = copy.deepcopy(config.BASE_NPC)
            npc.id = npc.id.format(i)
            npc.position = config.gen_init_position(self.map_center, config.NPC_INIT_RADIUS)
            npc.skills = config.gen_random_skills(config.NPC_SKILL_COUNT)
            npcs.append(npc)
        return npcs





