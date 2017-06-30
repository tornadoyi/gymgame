import os
from collections import namedtuple
import numpy as np
from easydict import EasyDict as edict

class _Node(object):
    def __init__(self, path, parent=None):
        self._path = path
        self._parent = parent
        self._dir = os.path.dirname(self._path)
        self._name = os.path.basename(self._path)

    @property
    def path(self): return self._path

    @property
    def dir(self): return self._dir

    @property
    def name(self): return self._name

    @property
    def parent(self): return self._parent



class _Structure(_Node):
    def __init__(self, *args, **kwargs):
        super(_Structure, self).__init__(*args, **kwargs)
        self._nodes = []


    @property
    def nodes(self): return self._nodes

    def add(self, node): self._nodes.append(node)


class _Array(_Structure): pass



class _Attribute(_Node):
    def __init__(self, path, parent, serializer, normalizer):
        super(_Attribute, self).__init__(path, parent)
        self._serializer = serializer
        self._normalizer = normalizer


    def serialize(self, *args, **kwargs): return self._serializer(*args, **kwargs)


    @property
    def normalizer(self): return self._normalizer

    @property
    def serializer(self): return self._serializer



def _size(v):
    ndims = len(np.shape(v))
    assert ndims <= 1
    return len(v) if ndims == 1 else 1



class SerializerKernel(object):
    class _serializer(object):
        pass

    class _normalizer(object):
        pass

    class s_type(_serializer):
        def __init__(self, t): self._t = t

        def __call__(self, v): return np.array(v, self._t)


    class s_float64(s_type):
        def __init__(self): super(SerializerKernel.s_float64, self).__init__(np.float64)

    class s_float32(s_type):
        def __init__(self): super(SerializerKernel.s_float32, self).__init__(np.float32)

    class n_none(_normalizer):
        def __call__(self, v, norm): return v

    class _n_tag(_normalizer):
        def __init__(self, tag): self._tag = tag

        @property
        def tag(self): return self._tag

        def get(self, norm):
            v = norm.tag.get(self._tag)
            if v is None: raise Exception('{0} is not existed in norm'.format(self._tag))
            return v

    class n_div_tag(_n_tag):
        def __call__(self, v, norm):
            n = self.get(norm)
            if (n == 0).any(): return n
            return v / n

    class _n_value(_normalizer):
        def __init__(self, v): self._v = v

    class n_div(_n_value):
        def __call__(self, v, norm): return v / self._v


    def __init__(self, o, path="/"):
        self._root_node = _Structure(path)
        self._nodes = {self._root_node.path: self._root_node}

        # temp
        self._cur_node = self._root_node
        self._obj_stack = [o]


    def serialize(self, o, norm, n_dict=None): return self._serialize_node(o, self._root_node, norm, n_dict)


    def serialize_node(self, o, path, norm, n_dict=None):
        node = self._nodes.get(path, None)
        if node is None: raise Exception('node {0} is not existed'.format(path))
        return self._serialize_node(o, node, norm, n_dict)


    def _serialize_node(self, o, root, norm, n_dict=None):
        serial = np.array([], np.float64)
        if type(root) == _Structure:
            for node in root.nodes:
                s = self._serialize_node(self.visit(o, node.name), node, norm, n_dict)
                serial = np.hstack([serial, s])

        elif type(root) == _Array:
            for i in range(len(o)):
                for node in root.nodes:
                    s = self._serialize_node(self.visit(o[i], node.name), node, norm, n_dict)
                    serial = np.hstack([serial, s])

        elif type(root) == _Attribute:
            s = root.serializer(o)
            serial = root.normalizer(s, norm) if norm is not None else s

            # normalize dict
            if n_dict is not None and isinstance(root.normalizer, SerializerKernel._n_tag):
                tag = root.normalizer.tag
                if tag not in n_dict:
                    n_dict[tag] = np.abs(s)
                else:
                    n_dict[tag] = np.max([np.abs(s), n_dict[tag]], axis=0)

        else:
            assert False

        return serial





    def add(self, k, serializer=None, normalizer=None):
        serializer = serializer or SerializerKernel.s_float64()
        normalizer = normalizer or SerializerKernel.n_none()

        # get value
        o = self._obj_stack[-1]
        v = getattr(o, k)
        if v is None: raise Exception('{0} is not existed in {1}'.format(k, type(o)))

        # create attribute
        param_path = self.create_path(self._cur_node.path, k)
        attr = _Attribute(param_path, self._cur_node, serializer, normalizer)
        self._cur_node.add(attr)


    def enter(self, name):
        # get value
        o = self._obj_stack[-1]
        v = getattr(o, name)
        if v is None: raise Exception('{0} is not existed in {1}'.format(name, type(o)))

        # create node
        path = self.create_path(self._cur_node.path, str(name))
        node = _Array(path, self._cur_node) if isinstance(v, (tuple, list)) else _Structure(path, self._cur_node)
        self._cur_node.add(node)
        self._cur_node = node
        self._nodes[node.path] = node

        # auto enter element when v is list or tuple
        if isinstance(v, (tuple, list)):
            if len(v) == 0: raise Exception('array {0} in {1} is empty, can not detect innner structure'.format(name, type(o)))
            v = v[0]

        # record obj
        self._obj_stack.append(v)


    def exit(self):
        self._cur_node = self._cur_node.parent
        self._obj_stack.pop()


    def visit(self, o, k):
        v = getattr(o, k)
        if v is None: raise Exception('{0} is not existed in {1}'.format(k, type(o)))
        return v


    def visits(self, o, path):
        if path == "/": return o
        params = path.split("/")[1:]
        for p in params:
            if isinstance(o, (tuple, list)):
                o = o[int(p)]
            else:
                o = getattr(o, p)
        return o

    def create_path(self, path, p):  return "{0}/{1}".format(path, p) if path != "/" else "{0}{1}".format(path, p)  #"#return os.path.join(*args).replace("\\", "/")


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
    def _select(self, k, *args): raise NotImplementedError("_select should be implemented")

    def _deserialize_action(self, data): raise NotImplementedError("deserialize_action should be implemented")


    def state_shape(self, index=0): return self._state_shapes[index]

    def on_start(self, game):
        # reset game
        game.reset()

        # create kernel
        self._kernel = SerializerKernel(game)
        self._select(self._kernel, game)

        # create normalized vector
        states = self.serialize_state(game)
        self._norm = self._gen_normalized_data(game)


        # get num state
        if isinstance(states, (tuple, list)):
            self._num_state = 1
            self._state_shapes = [states.shape]
        else:
            self._num_state = len(states)
            self._state_shapes = tuple([s.shape for s in states])


    def on_reset(self, game):
        self._norm = self._gen_normalized_data(game)


    def serialize_state(self, game): return self._kernel.serialize(game, self._norm)

    def serialize_state_to_dict(self, game):
        s_dict = {}
        self._kernel.serialize(game, self._norm, s_dict)
        return s_dict


    def deserialize_action(self, data): return self._deserialize_action(data)

    def _gen_normalized_data(self, game):
        # gen normalized tag
        tag_dict = {}
        self._kernel.serialize(game, self._norm, tag_dict)

        norm = edict(tag=tag_dict, game=game)
        return norm




