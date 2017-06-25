


class Factor(object):

    def __init__(self, relation):
        self._relation = relation


    @property
    def relation(self): return self._relation


    def __call__(self, *args, **kwargs): raise NotImplementedError('__call__ should be inplemented')

