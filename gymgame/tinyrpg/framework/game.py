from gymgame import framework
from .config import Action
from .object import NPC


class Game(framework.Game):
    def __init__(self, map_creator, player_creator, npc_creator):
        super(Game, self).__init__()
        self._map_creator = map_creator
        self._player_creator = player_creator
        self._npc_creator = npc_creator



    @property
    def map(self): return self._map


    def _reset(self):
        # init all modules
        self._map = self._map_creator()
        self._map.on_game_load(self)
        players = self._player_creator()
        npcs = self._npc_creator()

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


        # npc do
        ids = [o.id for o in self._map.finds(NPC)]
        for id in ids:
            npc = self._map.find(id, exception=False)
            if npc is None: continue
            npc.update()
