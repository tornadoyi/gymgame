from easydict import EasyDict as edict

def _enum(*args): return edict({n:n for n in args})

# note:

Attr = _enum(
    # object
    'id',
    'position',
    'direct',
    'speed',
    'radius',

    # character
    'hp',
    'max_hp',
    'mp',
    'max_mp',
    'camp',
    'recover_hp',
    'recover_mp',

    # bullet
    # hp
    # max_hp
    'max_range',
)


Action = _enum(
    'idle',
    'move_toward',
    'move_to',
    'cast_skill',
)


Relation = _enum(
    'any',
    'friend',
    'enemy',
)


Camp = [1 << i for i in range(32)]


def is_relation(relation, c1, c2):
    if relation == Relation.friend: return is_friend(c1, c2)
    elif relation == Relation.enemy: return is_enemy(c1, c2)
    return True


def is_enemy(c1, c2): return (c1 & c2) == 0

def is_friend(c1, c2): return not is_enemy(c1, c2)

def friend_camp(c): return c

def enemy_camp(c): return (2**32-1) ^ c





