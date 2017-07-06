import numpy as np
from easydict import EasyDict as edict


SERIALIZE_DTYPE = np.float64




class _SerializedKernel(object):

    @staticmethod
    def s_one_hot(v, len): return np.eye(len)[int(v)]

    @staticmethod
    def n_div_tag(v, norm, tag): return v if v == 0 else v / norm[tag]

    @staticmethod
    def n_div_value(v, norm, v2): return v / v2


    def __init__(self, norm=None, gen_norm=False, dtype=SERIALIZE_DTYPE):
        self._norm = norm
        self._gen_norm = gen_norm
        self._dtype = dtype

        self._do_norm = False if gen_norm or norm is None else True
        if self._gen_norm: self._norm = edict()

        # runtime
        self._cache = None #[object, data, list]
        self._cache_list = None


    @property
    def norm(self): return self._norm


    def do_object(self, o, func):
        if isinstance(o, (tuple, list)):
            def _loop(k, o):
                s = np.array([], dtype=self._dtype)
                for i in o:
                    a = self._do_object(i, func)
                    np.hstack([a, s])
                return s

            return self._do_object(o, _loop)

        else:
            return self._do_object(o, func)



    def do(self, v, serializer, normalizer, *args):
        s = v if serializer is None else serializer(v)
        n = s if normalizer is None or not self._do_norm else normalizer(s, self._norm, *args)

        if self._gen_norm and normalizer is self.n_div_tag:
            self._norm[args[0]] = n


        if not isinstance(n, np.ndarray):
            self._cache_list.append(n)
        else:
            self._merge_cache_list()
            self._cache[1] = np.hstack([self._cache[1], n])



    def _do_object(self, o, func):
        # save previous cache
        pre_cache = self._cache

        # create new cache
        self._cache_list = []
        self._cache = [o, np.array([], dtype=self._dtype), self._cache_list]

        # call do
        func(self, o)

        # merge to data
        self._merge_cache_list()

        # push data to parent data
        if pre_cache is not None: pre_cache[1] = np.hstack([pre_cache[1], self._cache[1]])

        # recover previous cache
        data = self._cache[1]
        self._cache = pre_cache
        self._cache_list = None if pre_cache is None else self._cache[2]

        return data


    def _merge_cache_list(self):
        if len(self._cache_list) == 0: return
        a = np.array(self._cache_list, dtype=self._dtype)
        self._cache[1] = np.hstack([self._cache[1], a])
        self._cache[2] = self._cache_list = []






class Serializer(object):
    def __init__(self, dtype=SERIALIZE_DTYPE):
        # on start
        self._dtype = dtype
        self._num_state = None
        self._state_shapes = None

        # on reset
        self._norm = None


    @property
    def num_state(self): return self._num_state

    # virtual
    def _serialize_state(self, k, game): raise NotImplementedError("_serialize_state should be implemented")


    def _deserialize_action(self, data): raise NotImplementedError("_deserialize_action should be implemented")


    def state_shape(self, index=0): return self._state_shapes[index]


    def deserialize_action(self, data): return self._deserialize_action(data)


    def serialize_state(self, game): return self._serialize_state(self._create_kernel(), game)


    def start(self, game): self._start(game)


    def reset(self, game): self._reset(game)


    def _start(self, game):

        # serialize
        states = self.serialize_state(game)

        # get num state
        if isinstance(states, (tuple, list)):
            self._num_state = len(states)
            self._state_shapes = tuple([s.shape for s in states])
        else:
            self._num_state = 1
            self._state_shapes = [states.shape]



    def _reset(self, game):
        k = self._create_kernel(gen_norm=True)
        self._serialize_state(k, game)
        self._norm = k.norm
        self._norm.game = game



    def _create_kernel(self, gen_norm=False): return _SerializedKernel(self._norm, gen_norm, dtype=self._dtype)