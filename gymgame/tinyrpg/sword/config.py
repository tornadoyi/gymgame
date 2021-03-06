import random
from easydict import EasyDict as edict
from gymgame.engine import *
from ..framework.config import *
from ..framework.skill import *
from ..framework.object.bullet import *



GAME_NAME = "tiny-rpg-sword-v0"

RENDER_MODE = "notebook"

MAP_SIZE = Vector2(10, 10)

MAP_BORDER = 1e-6

GRID_SIZE = None

GAME_PARAMS = edict()

NUM_PLAYERS = 1

NUM_NPC = 30

PLAYER_INIT_RADIUS = (0.0, 0.75)

NPC_INIT_RADIUS = (0.85, 0.9)

NPC_SKILL_COUNT = 1

AI = edict(defense_probability=0.2)


SKILL_DICT = {
    'normal_attack' : Skill(
        id = 'normal_attack',
        cast_time = 0.3,
        mp_cost = 0,
        target_required = True,
        target_relation = Relation.enemy,
        cast_distance = 0.5,
        target_factors = [Damage(30.0, Relation.enemy)]
    ),

    'normal_shoot' : Skill(
        id = 'normal_shoot',
        cast_time = 0.3,
        mp_cost = 0,
        bullet_emitter = SingleEmitter(
            speed=15.0, penetration=1.0, max_range=MAP_SIZE.x, radius=0.1,
            factors=[Damage(30.0, Relation.enemy)])
    ),
}

PLAYER_SKILL_LIST = SKILL_DICT.values()

NPC_SKILL_LIST = SKILL_DICT.values()


BASE_PLAYER = edict(
    id = "player-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 10.0,
    radius = 0.3,
    max_hp = 1000,
    camp = Camp[0],
    skills=PLAYER_SKILL_LIST,
)


BASE_NPC = edict(
    id = "npc-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 10.0,
    radius = 0.3,
    max_hp = 100.0,
    camp = Camp[1],
    skills=[]
)


def gen_init_position(center, r_range):
    r_range = np.array(r_range)
    minx, maxx = (MAP_SIZE.x - 1) / 2 * r_range
    miny, maxy = (MAP_SIZE.y - 1) / 2 * r_range
    r = Vector2(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
    direct = Vector2(*np.random.uniform(-1.0, 1.0, 2))
    return direct.normalized * r + center




def gen_npc_random_skills(count):
    all_skills = NPC_SKILL_LIST
    count = np.min([len(all_skills), count])
    indexes = random.sample(range(len(all_skills)), count)
    return [all_skills[idx] for idx in indexes]