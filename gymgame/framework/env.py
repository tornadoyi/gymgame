import gym
from gym import spaces
import numpy as np


class Environment(object):
    def __init__(self, game, serializer):
        self._game = game
        self._serializer = serializer

        # init serializer
        game.reset()
        self._serializer.start(game)

        # runtime
        self._states = []
        self._reset_count = 0


    @property
    def game(self): return self._game

    @property
    def serializer(self): return self._serializer

    @property
    def total_steps(self): return self._game.total_steps

    @property
    def steps(self): return self._game.steps

    @property
    def terminal(self): return self._game.terminal

    @property
    def state(self): return self._states[-1]

    @property
    def states(self): return self._states

    @property
    def reset_count(self): return self._reset_count


    def reset(self, *args, **kwargs): return self._reset(*args, **kwargs)

    def step(self, *args, **kwargs): return self._step(*args, **kwargs)

    def close(self, *args, **kwargs): return self._close(*args, **kwargs)

    def render(self, *args, **kwargs): return self._render(*args, **kwargs)


    def _reset(self, *args, **kwargs):
        self._reset_count += 1
        self._game.reset(*args, **kwargs)
        self._serializer.reset(self._game)
        s = self._serializer.serialize_state(self._game)
        self._states = [s]


    def _step(self, *args, **kwargs):
        self._game.step(*args, **kwargs)
        s = self._serializer.serialize_state(self._game)
        self._states.append(s)


    def _close(self, *args, **kwargs): return self._game.close(*args, **kwargs)

    def _render(self, *args, **kwargs): return self._game.render(*args, **kwargs)





class EnvironmentGym(Environment, gym.Env):

    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, initializer):
        Environment.__init__(self, *initializer())

        # observation and action space
        self.observation_space = spaces.Box(-np.inf, np.inf, self._serializer.state_shape())
        self.action_space = self._init_action_space()

        # runtime
        self._rewards = []

    @property
    def rewards(self): return self._rewards

    @property
    def reward(self): return self._rewards[-1]

    # virtual
    def _init_action_space(self): raise NotImplementedError("_reward should be implemented")

    def _reward(self): raise NotImplementedError("_reward should be implemented")

    def _info(self): return None

    def reset(self): return gym.Env.reset(self)

    def step(self, action): return gym.Env.step(self, action)

    def close(self): gym.Env.close(self)

    def render(self, mode='human', close=False): gym.Env.render(self, mode, close)


    def _reset(self):
        Environment._reset(self)
        self._rewards = []
        return self.state


    def _step(self, action):
        action = self._serializer.deserialize_action(action)
        Environment._step(self, action)
        s = self.state
        r = self._reward()
        t = self.terminal
        i = self._info()
        self._rewards.append(r)
        return s, r, t, i











