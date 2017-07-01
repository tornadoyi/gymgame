from gymgame.engine import extension
from .. import framework
from . import config
import numpy as np
from .data import Data


class Player(framework.Player):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._total_coins = 0
        self._total_hits = 0

        self._step_coins = 0
        self._step_hits = 0


    @property
    def total_coins(self): return self._total_coins

    @property
    def total_hits(self): return self._total_hits

    @property
    def step_coins(self): return self._step_coins

    @property
    def step_hits(self): return self._step_hits


    def hit(self, hits):
        self.attribute.hp -= hits
        self._step_hits += hits
        self._total_hits += hits


    def get_coin(self, count):
        if config.COIN_RECOVER_HP: self.attribute.hp += count
        self._step_coins += count
        self._total_coins += count


    def _update(self):
        self._step_coins = 0
        self._step_hits = 0




class Bullet(framework.NPC):

    def _update(self):
        self.move_toward(self.attribute.direct, bounds_limit=False)
        if self.attribute.hp > 1e-6 and self._map.in_bounds(self.attribute.position): return

        # revive
        if config.BULLET_REVIVE:
            self.revive()
        else:
            self.map.remove(self.attribute.id)


    def revive(self):
        self.attribute.position = config.gen_init_position(self.map.bounds.center, config.BULLET_INIT_RADIUS)
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
        self.attribute.position = config.gen_init_position(self.map.bounds.center, config.COIN_INIT_RADIUS)



class Map(framework.Map):

    @property
    def bullets(self): return [o for _, o in self._object_dict.items() if isinstance(o, Bullet)]

    @property
    def coins(self): return [o for _, o in self._object_dict.items() if isinstance(o, Coin)]



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
            if isinstance(npc, Bullet):
                player.hit(npc.hp)

            else:
                player.get_coin(npc.hp)

            npc.attribute.hp = 0






def make(): return Game(Data(Map, Player, Bullet, Coin), **config.GAME_PARAMS)