import gym
from gym import spaces
import numpy as np
from .env import EnvironmentGym, Environment
from collections import deque


class GymStackEnv(EnvironmentGym):
    """在生成state时返回历史上的4个state叠加, 从而保留运动轨迹
    Stack k last frames.
        Returns lazy array, which is much more memory efficient."""

    def __init__(self, initializer, frame_stack=4):
        super().__init__(initializer)
        self.frame_stack = frame_stack

        # 注意shape
        _s_shape = list(self._serializer.state_shape())
        _s_shape[-1] *= frame_stack
        self.observation_space = spaces.Box(-np.inf, np.inf, _s_shape)

        self.frames = deque([], maxlen=frame_stack)

    def _reset(self):
        Environment._reset(self)
        self._rewards = []
        for _ in range(self.frame_stack):
            self.frames.append(self.state)
        return self._get_stack_state()

    def _step(self, action):
        action = self._serializer.deserialize_action(action)
        Environment._step(self, action)
        s = self.state
        r = self._reward()
        t = self.terminal
        i = self._info()
        self._rewards.append(r)

        self.frames.append(s)

        return self._get_stack_state(), r, t, i

    def _get_stack_state(self):
        assert len(self.frames) == self.frame_stack
        return np.array(LazyFrames(list(self.frames)))


class LazyFrames(object):
    def __init__(self, frames):
        """This object ensures that common frames between the observations are only stored once.
        It exists purely to optimize memory usage which can be huge for DQN's 1M frames replay
        buffers.
        This object should only be converted to numpy array before being passed to the model.
        You'd not belive how complex the previous solution was."""
        self._frames = frames

    def __array__(self, dtype=None):
        out = np.concatenate(self._frames)
        if dtype is not None:
            out = out.astype(dtype)
        return out









