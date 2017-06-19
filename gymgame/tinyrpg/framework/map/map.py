from types import FunctionType, MethodType
from gymgame.engine import Vector2, Bounds2, Event
from ..object import *

# Events:
#   on_move(map, obj)

class Map(Event):
    def __init__(self, center, size):
        super(Map, self).__init__()
        self._bounds = Bounds2(Vector2(*center), Vector2(*size))
        self._object_dict = {}
        self._game = None

    @property
    def bounds(self): return self._bounds

    @property
    def game(self): return self._game

    @property
    def players(self): return self.finds(Player)

    @property
    def npcs(self): return self.finds(NPC)

    # events
    def on_game_load(self, game): self._game = game

    def _on_move(self, o): self.send_event('on_move', self, o)


    def add(self, o, position=None):
        self._object_dict[o.id] = o
        if position is not None: o.attribute.position = position
        o.enter_map(self)


    def remove(self, id):
        o = self._object_dict.pop(id, None)
        o.exit_map()


    def get(self, id): return self._object_dict.get(id)


    def find(self, id, exception=True):
        o =  self._object_dict.get(id, None)
        if o is None and exception: raise Exception("object {0} is not in map".format(id))
        return o


    def finds(self, t):
        if type(t) == FunctionType or type(t) == MethodType:
            return [o for o in self._object_dict.values() if t(o)]
        else:
            return [o for o in self._object_dict.values() if isinstance(o, t)]


    def move_toward(self, id, direct, bounds_limit=True):
        o = self.find(id)
        tgt_pos = o.attribute.position + direct.normalized * o.attribute.speed * self.game.delta_time
        # todo cross point
        o.attribute.position = tgt_pos
        self._on_move(o)




    def move_to(self, position, out_delete=False): pass