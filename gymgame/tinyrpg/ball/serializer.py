from .. import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):

    def deserialize_action(self, data):
        return (config.Action.idle)


    def _gen_normalized_data(self, v):
        return v


    def _select_character(self, k):
        k.add(Attr.hp, None, k.n_division)

