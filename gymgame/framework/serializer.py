import os
from collections import namedtuple
import numpy as np
from easydict import EasyDict as edict

class _Node(object):
    def __init__(self, path, start_pos, end_pos):
        self._path = path
        self._start_pos = start_pos
        self._end_pos = end_pos

    @property
    def path(self): return self._path

    @property
    def dir(self): return os.path.dirname(self._path)

    @property
    def name(self): return os.path.basename(self._path)

    @property
    def start_pos(self): return self._start_pos

    @property
    def end_pos(self): return self._end_pos

    @property
    def size(self): return self._end_pos - self._start_pos



class _Attribute(_Node):
    def __init__(self, path, start_pos, end_pos, serializer, normalizer):
        super(_Attribute, self).__init__(path, start_pos, end_pos)
        self._serializer = serializer
        self._normalizer = normalizer

    @property
    def normalizer(self): return self._normalizer

    @property
    def serializer(self): return self._serializer


class _Repeated(_Node): pass



class SerializerKernel(object):
    def __init__(self, o, path="/"):
        self._nodes = {}
        self._serialized_nodes = []
        self._serialized_size = 0

        # temp
        self._root = o
        self._cur_obj = None
        self._cur_path = path
        self._path_pos_stack = []


    @property
    def serialized_size(self): return self._serialized_size


    def node(self, path):
        if path[0] != "/": path = self.create_path("/", path)
        node = self._nodes.get(path)
        return node


    def slice(self, v, path):
        if path[0] != "/": path = self.create_path("/", path)
        node = self._nodes.get(path)
        if node is None: raise Exception("can not find path {0}".format(path))
        return v[node.start_pos : node.end_pos]



    def serialize(self, o, norm=None):
        serial = np.array([], np.float64)

        # serialize
        for i in range(len(self._serialized_nodes)):
            attr = self._serialized_nodes[i]
            v = self.visit(o, attr.path)
            s = attr.serializer(v, o)
            serial = np.hstack([serial, s])

        if norm is None: return serial


        # normalize
        assert self._size(serial) == self._size(norm)
        norm_serial = np.array([], np.float64)
        for i in range(len(self._serialized_nodes)):
            attr = self._serialized_nodes[i]
            s = serial[attr.start_pos: attr.end_pos]
            n = norm[attr.start_pos: attr.end_pos]
            ns = attr.normalizer(s, n, o)
            norm_serial = np.hstack([norm_serial, ns])

        return norm_serial


    def add(self, k, serializer = None, normalizer = None):
        serializer = serializer or self.s_float64
        normalizer = normalizer or self.n_none

        param_path = self.create_path(self._cur_path, k)
        rv = self.visit(self._root, param_path)
        sv = serializer(rv)
        nv = normalizer(sv, sv)
        s_size = self._size(sv)
        n_size = self._size(nv)

        assert s_size == n_size

        # calculate start location
        st = self._serialized_size
        self._serialized_size += s_size

        attr = _Attribute(param_path, st, self._serialized_size, serializer, normalizer)
        self._nodes[param_path] = attr
        self._serialized_nodes.append(attr)


    def adds(self, selector):
        o = self.visit(self._root, self._cur_path)
        assert isinstance(o, (list, tuple))
        for i in range(len(o)):
            self.enter(i)
            selector(self)
            self.exit()


    def s_float64(self, v, *args, **kwargs):
        if self._size(v) == 1: v = [v]
        v = np.array(v, np.float64)
        return v


    def n_none(self, v, n, *args, **kwargs): return v


    def n_division(self, v, n, *args, **kwargs):
        assert any(n) != 0
        return v / n


    @staticmethod
    def _size(v):
        ndims = len(np.shape(v))
        assert ndims <= 1
        return len(v) if ndims == 1 else 1


    def enter(self, name):
        self._cur_path = self.create_path(self._cur_path, str(name))
        self._path_pos_stack.append(self._serialized_size)


    def exit(self):
        self._cur_path = os.path.dirname(self._cur_path)
        if hasattr(self._nodes, self._cur_path): return
        o = self.visit(self._root, self._cur_path)
        st = self._path_pos_stack.pop()
        ed = self._serialized_size
        cls = _Repeated if isinstance(o, (tuple, list)) else _Node
        self._nodes[self._cur_path] = cls(self._cur_path, st, ed)


    def visit(self, o, path):
        if path == "/": return o
        params = path.split("/")[1:]
        for p in params:
            if isinstance(o, (tuple, list)):
                o = o[int(p)]
            else:
                o = getattr(o, p)
        return o


    def create_path(self, *args): return os.path.join(*args).replace("\\", "/")


class Serializer(object):
    def __init__(self):
        # on start
        self._num_state = None
        self._state_shapes = None

        # on reset
        self._norm = None



    @property
    def num_state(self): return self._num_state

    # virtual
    def _gen_normalized_data(self, v, *args): raise NotImplementedError("_gen_normalized_data should be implemented")

    def _select(self, k, *args): raise NotImplementedError("_select should be implemented")


    def state_shape(self, index=0): return self._state_shapes[index]

    #def serialize_action(self, action): raise NotImplementedError("serialize_action should be implemented")

    def deserialize_action(self, data): raise NotImplementedError("deserialize_action should be implemented")


    def on_start(self, game):
        # reset game
        game.reset()

        # create kernel
        self._kernel = SerializerKernel(game)
        self._select(self._kernel, game)

        # create normalized vector
        states = self.serialize_state(game)
        self._norm = self._gen_normalized_data(states, game)


        # get num state
        if isinstance(states, (tuple, list)):
            self._num_state = 1
            self._state_shapes = [states.shape]
        else:
            self._num_state = len(states)
            self._state_shapes = tuple([s.shape for s in states])


    def on_reset(self, game):
        states = self.serialize_state(game)
        self._norm = self._gen_normalized_data(states, game)


    def serialize_state(self, game): return self._kernel.serialize(game, self._norm)





