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



def gen_init_position(r_range):
    r_range = np.array(r_range)
    minx, maxx = MAP_SIZE.x / 2 * r_range
    miny, maxy = MAP_SIZE.y / 2 * r_range
    r = Vector2(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
    direct = Vector2(*np.random.uniform(-1.0, 1.0, 2))
    return direct.normalized * r



def gen_npc_direct(src_pos, dst_pos):
    def _aim():
        direct = dst_pos - src_pos
        angle = np.random.uniform(-NPC_DIRECT_SHAKE_ANGLE, NPC_DIRECT_SHAKE_ANGLE)
        return direct.rotate(angle)

    def _random(): return Vector2(*np.random.uniform(-1, 1, 2))

    if np.random.rand() < NPC_AIM_PROBABILITY:
        return _aim()
    else:
        return _random()



_last_players = None

def gen_players():
    global _last_players
    _last_players = []
    for i in range(NUM_PLAYERS):
        player = copy.deepcopy(BASE_PLAYER)
        player.id = player.id.format(i)
        player.position = gen_init_position(PLAYER_INIT_RADIUS)
        _last_players.append(player)
    return _last_players



def gen_npcs():
    npcs = []
    player = _last_players[0]

    for i in range(NUM_NPC):
        # position and direct
        position = gen_init_position(NPC_INIT_RADIUS)
        direct = gen_npc_direct(position, player.position)

        npc = copy.deepcopy(BASE_NPC)
        npc.id = npc.id.format(i)
        npc.position = position
        npc.direct = direct
        npcs.append(npc)

    return npcs



