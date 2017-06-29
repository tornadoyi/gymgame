import copy
from gymgame.engine import *
from ..framework.config import *

GAME_NAME = "tiny-rpg-man-v0"

MAP_CENTER = Vector2(0, 0)
MAP_SIZE = Vector2(10, 10)

GAME_PARAMS = edict()

NUM_PLAYERS = 1

NUM_NPC = 30

NPC_AIM_PROBABILITY = 0.3

NPC_DIRECT_SHAKE_ANGLE = 30

PLAYER_INIT_RADIUS = (0.0, 0.25)

NPC_INIT_RADIUS = (0.75, 1.0)


BASE_PLAYER = edict(
    id = "player-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 12.0,
    radius = 0.5,
    max_hp = 1,
    hp = 1,
)

BASE_NPC = edict(
    id = "npc-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 10.0,
    radius = 0.3,
    max_hp = 1,
    hp = 1,
)






