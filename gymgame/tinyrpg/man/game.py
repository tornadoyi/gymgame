from .. import framework
from ..framework import Character, NPC, Player
from . import config

class Map(framework.Map):
    def __init__(self):
        super(Map, self).__init__(config.MAP_CENTER, config.MAP_SIZE)


    def _on_move(self, o):
        char_list = self.finds(Player) if type(o) is NPC else self.finds(NPC)

        o_pos, o_radius = o.attribute.position, o.attribute.radius
        for char in char_list:
            pos, radius = char.attribute.position,  char.attribute.radius
            d = pos.distance(o_pos)
            if d > o_radius + radius: continue

            # on collision
            if o.attribute.hp > char.attribute.hp:
                o.attribute.hp += char.attribute.hp
                self.remove(char.attribute.id)

            else:
                char.attribute.hp += o.attribute.hp
                self.remove(o.attribute.id)
                break


class NPCExtension(object):

    @staticmethod
    def _update(self):
        # find weak and strong
        players = self._map.finds(Player)
        weak = strong = None
        for player in players:
            if self.attribute.hp < player.attribute.hp:
                strong = strong or player
                strong = strong if strong.attribute.hp > player.attribute.hp else player

            else:
                weak = weak or player
                weak = weak if weak.attribute.hp < player.attribute.hp else player

        # greedy for week
        if weak is not None:
            self.move_to(weak.attribute.position)
            return


        if strong is not None:
            direct = self.attribute.position - strong.attribute.position
            self.move_toward(direct)
            return


NPC._update = NPCExtension._update


class Game(framework.Game):

    def _check_terminal(self):
        players = self._map.finds(Player)
        npcs = self._map.finds(NPC)
        return len(players) == 0 or len(npcs) == 0



def make():
    return Game(
        lambda : Map(),
        lambda : [Player(data) for data in config.PLAYERS],
        lambda: [NPC(data) for data in config.NPCS]
    )