import random
from easydict import EasyDict as edict
from gymgame.engine import *
from ..framework.config import *
from ..framework.skill import *
from ..framework.object.bullet import *



GAME_NAME = "tiny-rpg-sword-v0"


MAP_SIZE = Vector2(10, 10)

GAME_PARAMS = edict()

NUM_PLAYERS = 1

NUM_NPC = 1

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


BASE_PLAYER = edict(
    id = "player-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 10.0,
    radius = 0.3,
    max_hp = 100,
    camp = Camp[0],
    skills=list(SKILL_DICT.values())
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




def gen_random_skills(count):
    all_skills = list(SKILL_DICT.values())
    count = np.min([len(all_skills), count])
    indexes = random.sample(range(len(all_skills)), count)
    return [all_skills[idx] for idx in indexes]