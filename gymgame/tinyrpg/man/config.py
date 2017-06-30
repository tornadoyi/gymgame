import copy
from gymgame.engine import *
from ..framework.config import *

GAME_NAME = "tiny-rpg-man-v0"


MAP_SIZE = Vector2(10, 10)

GAME_PARAMS = edict()

NUM_PLAYERS = 1

NUM_BULLET = 30

NUM_COIN = 30

BULLET_AIM_PROBABILITY = 0.3

BULLET_DIRECT_SHAKE_ANGLE = 30

PLAYER_INIT_RADIUS = (0.0, 0.25)

BULLET_INIT_RADIUS = (0.75, 1.0)

COIN_INIT_RADIUS = (0.3, 1.0)

BULLET_REVIVE = True

COIN_REVIVE = True

COIN_RECOVER_HP = False



BASE_PLAYER = edict(
    id = "player-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 12.0,
    radius = 0.5,
    max_hp = 1,
)


BASE_BULLET = edict(
    id = "bullet-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 10.0,
    radius = 0.1,
    max_hp = 1,
)


BASE_COIN = edict(
    id = "coin-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    radius = 0.1,
    max_hp = 1,
)



def gen_init_position(center, r_range):
    r_range = np.array(r_range)
    minx, maxx = (MAP_SIZE.x - 1) / 2 * r_range
    miny, maxy = (MAP_SIZE.y - 1) / 2 * r_range
    r = Vector2(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
    direct = Vector2(*np.random.uniform(-1.0, 1.0, 2))
    return direct.normalized * r + center



def gen_aim_direct(src_pos, dst_pos, probability=BULLET_AIM_PROBABILITY, shake_angle=BULLET_DIRECT_SHAKE_ANGLE):
    def _aim():
        direct = dst_pos - src_pos
        angle = np.random.uniform(-shake_angle, shake_angle)
        return direct.rotate(angle)

    def _random():
        return Vector2(*np.random.uniform(-1, 1, 2))

    if np.random.rand() < probability:
        return _aim()
    else:
        return _random()

