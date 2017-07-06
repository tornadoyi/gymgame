

from gymgame.engine import Vector2, extension
from gymgame.tinyrpg import man

config = man.config

Attr = config.Attr

GAME_NAME = config.GAME_NAME


# env constant
config.MAP_SIZE = Vector2(30, 30)

config.GRID_SIZE = config.MAP_SIZE

config.NUM_BULLET = 0

config.NUM_COIN = 30

config.COIN_WANDER = True



@extension(man.Serializer)
class SerializerExtension():

    DIRECTS = [Vector2.up, Vector2.right, Vector2.down, Vector2.left]

    def _deserialize_action(self, data):
        direct = SerializerExtension.DIRECTS[data]
        actions = [('player-0', config.Action.move_toward, direct, None)]
        return actions



