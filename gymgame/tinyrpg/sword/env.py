from gymgame import framework
from gym import envs, spaces
from gym.envs import register
from . import config
from . import game
from .serializer import Serializer
from gymgame.tinyrpg.framework.render import Renderer
# from .render import Render



class EnvironmentGym(framework.EnvironmentGym):
    def __init__(self, *args, **kwargs):
        super(EnvironmentGym, self).__init__(*args, **kwargs)

    def _init_action_space(self): return spaces.Discrete(1)

    def _reward(self): return 0

    def close(self, *args, **kwargs): pass  # close will trigger render(don't need it in many case)

    def _render(self, *args, **kwargs):
        if self._game.renderer is None:
            self._game.renderer = Renderer(self._game, config.RENDER_MODE)
        else:
            self._game.render()



register(
    id=config.GAME_NAME,
    entry_point='gymgame.tinyrpg.sword:EnvironmentGym',
    max_episode_steps=1e+10,
    kwargs={'initializer': lambda: (game.make(), Serializer(config.GRID_SIZE)) }
)