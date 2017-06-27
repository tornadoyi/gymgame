from .. import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):

    def _deserialize_action(self, data): return []


    def _select_character(self, k):
        self._select_object(k)
        k.add(Attr.hp, None, k.n_div_tag(Attr.hp))

