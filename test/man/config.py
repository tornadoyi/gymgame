

from gymgame.engine import Vector2, extension
from gymgame.tinyrpg import man

config = man.config

Attr = config.Attr

GAME_NAME = config.GAME_NAME

# env constant

config.GAME_PARAMS.fps = 1

config.MAP_SIZE = Vector2(10, 10)

config.NUM_BULLET = 40

config.NUM_COIN = 0

config.BULLET_INIT_RADIUS = (0.99, 1.0)

config.COIN_WANDER = False

config.BASE_PLAYER.speed = 0.5

config.BASE_PLAYER.radius = 0.3

config.BASE_BULLET.speed = 0.5

config.BASE_BULLET.radius = 0.1


@extension(man.Serializer)
class SerializerExtension():

    DIRECTS = [Vector2.up, Vector2.right, Vector2.down, Vector2.left]

    def _deserialize_action(self, data):
        direct = SerializerExtension.DIRECTS[data]
        actions = [('player-0', config.Action.move_toward, direct, None)]
        return actions



