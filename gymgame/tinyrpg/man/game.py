from gymgame.engine import extension
from .. import framework
from . import config
import numpy as np
from .data import Data



class Bullet(framework.NPC):

    def _update(self):
        self.move_toward(self.attribute.direct)
        if self.attribute.hp > 1e-6 and self._map.in_bounds(self.attribute.position): return

        # revive
        if config.BULLET_REVIVE:
            self.revive()
        else:
            self.map.remove(self.attribute.id)


    def revive(self):
        self.attribute.position = config.gen_init_position(config.BULLET_INIT_RADIUS)
        players = self.map.players
        if len(players) != 0:
            index = np.random.randint(0, len(players))
            player = players[index]
            self.attribute.hp = self.attribute.max_hp
            self.attribute.direct = config.gen_aim_direct(self.attribute.position, player.attribute.position)


class Coin(framework.NPC):
    def _update(self):
        if self.attribute.hp > 1e-6: return

        # revive
        if config.COIN_REVIVE:
            self.revive()
        else:
            self.map.remove(self.attribute.id)


    def revive(self):
        self.attribute.hp = self.attribute.max_hp
        self.attribute.position = config.gen_init_position(config.COIN_INIT_RADIUS)



class Game(framework.Game):

    def _check_terminal(self):
        players = self._map.players
        if len(self.map.npcs) == 0: return True

        for player in players:
            if player.attribute.hp > 1e-6: return False

        return True


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
            if isinstance(npc, Bullet): player.attribute.hp -= npc.attribute.hp
            npc.attribute.hp = 0






def make(): return Game(Data(framework.Map, framework.Player, Bullet, Coin), **config.GAME_PARAMS)