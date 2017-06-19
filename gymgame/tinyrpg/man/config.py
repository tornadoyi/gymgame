from gymgame.engine import *
from ..framework.config import *

GAME_NAME = "tiny-rpg-man-v0"

MAP_CENTER = Vector2(0, 0)
MAP_SIZE = Vector2(10, 10)

MAP_BOUND = Bounds2(MAP_CENTER, MAP_SIZE)

NPCS = [
    edict(
        id = "npc-01",
        position = Vector2(-3, -3),
        speed = 1.0,
        radius = 0.5,
        hp = 10
    )

]


PLAYERS = [
    edict(
        id = "player-01",
        position = Vector2(3, 3),
        speed = 2.0,
        radius = 0.5,
        hp = 15
    )
]