from gymgame import framework
from gym import envs, spaces
from gym.envs import register
from . import config
from . import game
from .serializer import Serializer



class EnvironmentGym(framework.EnvironmentGym):

    def _init_action_space(self): return spaces.Discrete(1)

    def _reward(self):
        return 0


    def _render(self, *args, **kwargs): pass


    def _close(self, *args, **kwargs): pass





register(
    id=config.GAME_NAME,
    entry_point='gymgame.tinyrpg.ball:EnvironmentGym',
    max_episode_steps=1e+10,
    kwargs={'initializer': lambda: (game.make(), Serializer()) }
)