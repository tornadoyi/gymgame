from gymgame import framework
from .config import Action
from .object import NPC


class Game(framework.Game):
    def __init__(self, data,  **kwargs):
        super(Game, self).__init__(**kwargs)
        self._data = data


    @property
    def data(self): return self._data


    @property
    def map(self): return self._map



    def _reset(self):
        # init all modules
        self._data.reset()
        self._map = self._data.map
        self._map.on_game_load(self)
        players = self._data.players
        npcs = self._data.npcs

        # add objects to map
        for o in list(players + npcs): self._map.add(o)



    def _step(self, actions):
        # actions: action list with struct (id, type, params...)

        # player do
        for a in actions:
            id, type, params = a[0], a[1], a[2:]
            player = self._map.find(id)
            f_action = getattr(player, type)
            f_action(*params)


        # all do
        for obj in self._map.objects:
            obj = self._map.find(obj.attribute.id, exception=False)
            if obj is None: continue
            obj.update()

