from gymgame.engine import extension
from .. import framework
from ..framework import Character, NPC, Player
from . import config

class Map(framework.Map):
    def __init__(self):
        super(Map, self).__init__(config.MAP_CENTER, config.MAP_SIZE)


    def _on_move(self, o):
        def _check_collision(a, b):
            d = a.attribute.position.distance(b.attribute.position)
            return (a.attribute.radius + b.attribute.radius) > d

        npcs = self.npcs
        if type(o) == NPC:
            npc = o
            for player in self.players:
                if player.attribute.hp < 1e-6: continue
                if not _check_collision(npc, player): continue
                player.attribute.hp -= npc.attribute.hp
                npc.attribute.hp = 0
                break

        elif type(o) == Player:
            player = o
            for npc in npcs:
                if not _check_collision(npc, player): continue
                player.attribute.hp -= npc.attribute.hp
                npc.attribute.hp = 0

        else: raise Exception("invalid object type {0}".format(type(o)))



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




def make():
    return Game(
        lambda : Map(),
        lambda : [Player(data) for data in config.gen_players()],
        lambda: [NPC(data) for data in config.gen_npcs()]
    )