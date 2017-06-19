from .. import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):

    def deserialize_action(self, data):
        return (config.PLAYER_IDS[0], config.Action.idle)


    def _select_character(self, k):
        k.add(Attr.position, None, k.n_division)

