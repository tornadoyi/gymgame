import copy
from .object import Player, NPC
from .map import Map


class Data(object):
    def __init__(self, map_cls = None, player_cls=None, npc_cls=None):
        self._map_cls = map_cls or Map
        self._player_cls = player_cls or Player
        self._npc_cls = npc_cls or NPC

        # runtime
        self._map_info = None
        self._npc_infos = None
        self._player_infos = None


        self._map = None
        self._npcs = None
        self._players = None


    @property
    def map(self): return self._map

    @property
    def players(self): return self._players

    @property
    def npcs(self): return self._npcs

    # virtual
    def _create_map_info(self): raise NotImplementedError('_create_map should be implemented')

    def _create_player_infos(self): return []

    def _create_npc_infos(self): return []


    def reset(self):
        # map
        self._map_info = copy.deepcopy(self._create_map_info())
        self._map = self._map_cls(**self._map_info)

        # players
        self._players = []
        self._player_infos = copy.deepcopy(self._create_player_infos())
        for info in self._player_infos: self._players.append(self._player_cls(info))

        # npcs
        self._npcs = []
        self._npc_infos = copy.deepcopy(self._create_npc_infos())
        for info in self._npc_infos: self._npcs.append(self._npc_cls(info))

