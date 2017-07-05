
import numpy as np
from gymgame.engine import Vector2, extension
from gymgame.tinyrpg import man

config = man.config

Attr = config.Attr

GAME_NAME = config.GAME_NAME


# env constant
config.MAP_SIZE = Vector2(30, 30)

config.GRID_SIZE = config.MAP_SIZE

config.NUM_BULLET = 50

config.NUM_COIN = 50



@extension(man.Serializer)
class SerializerExtension():

    DIRECTS = [Vector2.up, Vector2.right, Vector2.down, Vector2.left]

    def _deserialize_action(self, data):
        skill_idex = np.argmax(data[0:3])
        target_idx = np.argmax(data[3:])

        if skill_idex == 0: skillid = 'normal_attakc'

        target = game.map.find('npc-{0}'.format(target_idx))

        #direct = SerializerExtension.DIRECTS[data]
        actions = [('player-0', config.Action.cast_skill, skillid, target)]
        return actions



