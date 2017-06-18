import gym
from gym import spaces
import numpy as np


class Environment(object):
    def __init__(self, game, serializer):
        self._game = game
        self._serializer = serializer

        # init serializer
        self._serializer.on_start(game)

        # runtime
        self._state = None


    @property
    def total_steps(self): return self._game.total_steps

    @property
    def steps(self): return self._game.steps

    @property
    def terminal(self): return self._game.terminal

    @property
    def state(self): return self._state


    def reset(self, *args, **kwargs): return self._reset(*args, **kwargs)

    def step(self, *args, **kwargs): return self._step(*args, **kwargs)

    def close(self, *args, **kwargs): return self._close(*args, **kwargs)

    def render(self, *args, **kwargs): return self._render(*args, **kwargs)


    def _reset(self, *args, **kwargs):
        self._game.reset(*args, **kwargs)
        self._state = self._serializer.serialize_state(self._game)


    def _step(self, *args, **kwargs):
        self._game.step(*args, **kwargs)
        self._state = self._serializer.serialize_state(self._game)


    def _close(self, *args, **kwargs): return self._game.close(*args, **kwargs)

    def _render(self, *args, **kwargs): return self._game.render(*args, **kwargs)





class EnvironmentGym(Environment, gym.Env):
    def __init__(self, initializer):
        Environment.__init__(self, *initializer())

        # observation and action space
        self.observation_space = spaces.Box(-np.inf, np.inf, self._serializer.state_shape())
        self.action_space = self._init_action_space()



    # virtual
    def _init_action_space(self): raise NotImplementedError("_reward should be implemented")

    def _reward(self): raise NotImplementedError("_reward should be implemented")

    def reset(self): return gym.Env.reset(self)

    def step(self, action): return gym.Env.step(self, action)

    def close(self): gym.Env.close(self)

    def render(self, mode='human', close=False): gym.Env.render(self, mode, close)


    def _reset(self):
        Environment._reset(self)
        return self._state


    def _step(self, action):
        Environment._step(self, action)
        s = self._state
        r = self._reward()
        t = self.terminal
        return s, r, t, None











