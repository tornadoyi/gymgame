from gymgame import framework
from gym import envs, spaces
from gym.envs import register
from . import config
from . import game
from .serializer import Serializer
from .render import Render




class EnvironmentGym(framework.EnvironmentGym):
    def __init__(self, *args, **kwargs):
        super(EnvironmentGym, self).__init__(*args, **kwargs)
        self._window = Render(self)

    def _init_action_space(self): return spaces.Discrete(1)

    def _reward(self): return 0
        
    def _close(self, *args, **kwargs): pass

    def _render(self, *args, **kwargs):
        if not hasattr(self, '_window'): return
        self._window.update()



register(
    id=config.GAME_NAME,
    entry_point='gymgame.tinyrpg.man:EnvironmentGym',
    max_episode_steps=1e+10,
    kwargs={'initializer': lambda: (game.make(), Serializer()) }
)