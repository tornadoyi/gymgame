from .. import framework
from ..framework import Character, NPC, Player
from . import config

class Map(framework.Map):
    def __init__(self):
        super(Map, self).__init__(config.MAP_CENTER, config.MAP_SIZE)


    def _on_move(self, o):

        def _check_collision(a, b):
            d = a.attribute.position.distance(b.attribute.position)
            return a.attribute.radius + b.attribute.radius < d

        player = self.players[0]
        npcs = self.npcs
        if type(o) == NPC:
            if _check_collision(o, player): player.attribute.hp = 0

        elif type(o) == Player:
            for npc in npcs:
                if not _check_collision(npc, player): continue
                o.attribute.hp = 0
                break

        else: raise Exception("invalid object type {0}".format(type(o)))


class NPCExtension(object):
    @staticmethod
    def move_toward(self, direct): self._map.move_toward(self.attribute.id, direct, bounds_limit=False)

    @staticmethod
    def move_to(self, position): self._map.move_to(self.attribute.id, position, bounds_limit=False)

    @staticmethod
    def _update(self): self.move_toward(self.attribute.direct)


NPC._update = NPCExtension._update
NPC.move_toward = NPCExtension.move_toward
NPC.move_to = NPCExtension.move_to


class Game(framework.Game):

    def _check_terminal(self):
        players = self._map.finds(Player)
        return players[0].attribute.hp < 1e-6




def make():
    return Game(
        lambda : Map(),
        lambda : [Player(data) for data in config.PLAYERS],
        lambda: [NPC(data) for data in config.NPCS]
    )