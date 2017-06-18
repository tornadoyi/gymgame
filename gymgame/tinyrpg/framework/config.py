from easydict import EasyDict as edict

def _enum(*args): return edict({n:n for n in args})


Attr = _enum(
    # object
    'id',
    'position',
    'speed',
    'radius',

    # character
    'hp',
    'max_hp',
    'mp',
    'max_mp',
)


Action = _enum(
    'idle',
    'move_toward',
    'move_to',
    'do_skill',
)


