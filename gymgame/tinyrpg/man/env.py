import numpy as np
from gymgame import framework
from gymgame.framework import env_stack
from gym import envs, spaces
from gym.envs import register
from . import config
from . import game
from .serializer import Serializer
from .render_bokehserve import Render


class EnvironmentGym(env_stack.GymStackEnv):
    def __init__(self, *args, **kwargs):
        super(EnvironmentGym, self).__init__(*args, **kwargs)
        self._window = None

    def _init_action_space(self): return spaces.Box(low=-1, high=1, shape=(2,))


    def close(self, *args, **kwargs): pass  # close will trigger render(don't need it in many case)


    def _render(self, *args, **kwargs):
        if self._window is None:
            self._window = Render(self)
        else:
            self._window.update()


    def _reward(self):
        players = self.game.map.players
        hits = np.array([player.step_hits for player in players])
        coins = np.array([player.step_coins for player in players])
        r = coins - hits
        return r[0] if len(r) == 1 else r



register(
    id=config.GAME_NAME,
    entry_point='gymgame.tinyrpg.man:EnvironmentGym',
    kwargs={'initializer': lambda: (game.make(), Serializer(config.GRID_SIZE)) }
)