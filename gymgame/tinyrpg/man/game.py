from gymgame.engine import extension
from .. import framework
from ..framework import Character, NPC, Player
from . import config
import numpy as np


class Map(framework.Map):
    def __init__(self):
        super(Map, self).__init__(config.MAP_CENTER, config.MAP_SIZE)



@extension(NPC)
class NPCExtension(object):
    def move_toward(self, direct): self._map.move_toward(self.attribute.id, direct, bounds_limit=False)

    def move_to(self, position): self._map.move_to(self.attribute.id, position, bounds_limit=False)

    def _update(self):
        self.move_toward(self.attribute.direct)
        if self.attribute.hp < 1e-6 or not self._map.in_bounds(self.attribute.position):
            self._map.remove(self.attribute.id)



class Game(framework.Game):

    def _check_terminal(self):
        players = self._map.finds(Player)
        return players[0].attribute.hp < 1e-6 or len(self.map.npcs) == 0


    def _step(self, actions):
        super(Game, self)._step(actions)
        # objects
        npcs = self.map.npcs
        players = self.map.players
        if len(npcs) == 0 or len(players) == 0: return

        # position
        npcs_pos = np.array([npc.attribute.position for npc in npcs])
        players_pos = np.array([player.attribute.position for player in players])

        # radius
        npcs_radius = np.array([npc.attribute.radius for npc in npcs])
        players_radius = np.array([player.attribute.radius for player in players])

        # distance square
        npcs_pos = npcs_pos.reshape([1, npcs_pos.shape[0], npcs_pos.shape[1]])
        players_pos = players_pos.reshape([players_pos.shape[0], 1, players_pos.shape[1]])
        v = npcs_pos - players_pos
        d2 = np.sum(np.square(v), axis=2)

        # sum radius square
        npcs_radius = npcs_radius.reshape([1, npcs_radius.shape[0]])
        players_radius = players_radius.reshape([players_radius.shape[0], 1])
        r = npcs_radius + players_radius
        r2 = np.square(r)

        # check collission
        cond = np.where(r2 > d2)
        cond = list(zip(cond[0].tolist(), cond[1].tolist()))
        for i_player, i_npc in cond:
            player = players[i_player]
            npc = npcs[i_npc]
            player.attribute.hp -= npc.attribute.hp
            npc.attribute.hp = 0



def make():
    return Game(
        lambda : Map(),
        lambda : [Player(data) for data in config.gen_players()],
        lambda: [NPC(data) for data in config.gen_npcs()],
        **config.GAME_PARAMS
    )