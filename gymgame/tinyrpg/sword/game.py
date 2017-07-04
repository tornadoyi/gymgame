import numpy as np
from .. import framework
from . import config
from .data import Data
from .ai import AI


class Map(framework.Map):
    pass


class Player(framework.Player):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)



class NPC(framework.NPC):
    def __init__(self, *args, **kwargs):
        super(NPC, self).__init__(*args, **kwargs)
        self._ai = AI(self)


    def _update(self):
        if super(NPC, self)._update(): return
        return self._ai()






class Game(framework.Game):

    def _check_terminal(self):
        players = self._map.finds(Player)
        return players[0].attribute.hp < 1e-6 or len(self.map.npcs) == 0


    def _step(self, actions):
        super(Game, self)._step(actions)
        # objects
        chars = self.map.players + self.map.npcs
        bullets = self.map.bullets
        if len(bullets) == 0 or len(chars) == 0: return


        # position
        bullets_pos = np.array([bullet.attribute.position for bullet in bullets])
        chars_pos = np.array([char.attribute.position for char in chars])

        # radius
        bullets_radius = np.array([bullet.attribute.radius for bullet in bullets])
        chars_radius = np.array([char.attribute.radius for char in chars])

        # distance square
        bullets_pos = bullets_pos.reshape([1, bullets_pos.shape[0], bullets_pos.shape[1]])
        chars_pos = chars_pos.reshape([chars_pos.shape[0], 1, chars_pos.shape[1]])
        v = bullets_pos - chars_pos
        d2 = np.sum(np.square(v), axis=2)

        # sum radius square
        bullets_radius = bullets_radius.reshape([1, bullets_radius.shape[0]])
        chars_radius = chars_radius.reshape([chars_radius.shape[0], 1])
        r = bullets_radius + chars_radius
        r2 = np.square(r)

        # check collission
        cond = np.where(r2 > d2)
        cond = list(zip(cond[0].tolist(), cond[1].tolist()))
        for i_char, i_bullet in cond:
            char = chars[i_char]
            bullet = bullets[i_bullet]
            char.attribute.hp -= bullet.attribute.hp
            bullet.attribute.hp = 0



def make(): return Game(Data(Map, Player, NPC), **config.GAME_PARAMS)