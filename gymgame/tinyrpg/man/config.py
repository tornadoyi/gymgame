from gymgame.engine import *
from ..framework.config import *

GAME_NAME = "tiny-rpg-man-v0"

MAP_CENTER = Vector2(0, 0)
MAP_SIZE = Vector2(10, 10)

MAP_BOUND = Bounds2(MAP_CENTER, MAP_SIZE)

NUM_NPC = 4

PLAYER_RADIUS = 0.5

NPC_RADIUS = 0.3

PLAYER_IDS = ["player-0"]


_last_players = None

def gen_players():
    global _last_players
    _last_players = [
        edict(
            id = PLAYER_IDS[0],
            position = Vector2(0, 0),
            direct = Vector2(0, 0),
            speed = 2.0,
            radius = 0.5,
            hp = 15
        )
    ]
    return _last_players



def gen_npcs():
    npcs = []
    rmin = (PLAYER_RADIUS + NPC_RADIUS) * 2
    rmax = MAP_SIZE.x / 2

    player = _last_players[0]

    for i in range(NUM_NPC):
        # position
        r = np.random.uniform(rmin, rmax)
        x, y = np.random.uniform(-1.0, 1.0, 2)
        direct = Vector2(x, y)
        position = direct.normalized * r

        # direct
        direct = player.position - position

        npc = edict(
            id="npc-{0}".format(i),
            position=position,
            direct=direct,
            speed=1.0,
            radius=NPC_RADIUS,
            hp=15
        )

        npcs.append(npc)

    return npcs



