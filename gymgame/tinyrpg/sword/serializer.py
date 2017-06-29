from .. import framework
from . import config

Attr = config.Attr

class Serializer(framework.Serializer):

    def _deserialize_action(self, data): return []


    def _select_character(self, k):
        super(Serializer, self).__init__()

