import numpy as np
from easydict import EasyDict as edict
from bokeh.io import output_notebook, show, push_notebook
from bokeh.plotting import figure
from bokeh.layouts import gridplot


class RenderBase():

    def __call__(self, env, game): pass

    def initialize(self, env, game, plot_dict): pass


class NoneRender(RenderBase):
    pass


class ObjectRender(RenderBase):
    pass


class CharacterRender(ObjectRender):
    pass


class NPCRender(CharacterRender):
    pass


class PlayerRender(CharacterRender):
    pass


class BulletRender(ObjectRender):
    pass



class MapRender(RenderBase):
    def __init__(self, witdh=600, height=600):
        self._with = witdh
        self._height = height

    @property
    def plot_map(self): return self._plt_map


    def initialize(self, env, game, plot_dict):
        map = game.map
        # create figure
        bounds = map.bounds
        x_min, x_max = int(bounds.min.x), int(bounds.max.x)
        y_min, y_max = int(bounds.min.y), int(bounds.max.y)

        self._plt_map = figure(
            plot_width=self._with,
            plot_height=self._height,
            x_range=(x_min, x_max),
            y_range=(y_min, y_max),
        )

        plot_dict.map = self._plt_map







class Render(object):
    def __init__(self, env,
                 map_render=None, npc_render=None, player_render=None, bullet_render=None,
                 custom_renders=[]):

        self._env = env
        self._game = env.game
        self._map_render = map_render or MapRender()
        self._npc_render = npc_render or NPCRender()
        self._player_render = player_render or PlayerRender()
        self._bullet_render = bullet_render or BulletRender()
        self._custom_renders = custom_renders
        self._plot_dict = edict()

        # output_notebook
        output_notebook()


        # initialize
        self._map_render.initialize(self._env, self._game, self._plot_dict)
        self._npc_render.initialize(self._env, self._game, self._plot_dict)
        self._player_render.initialize(self._env, self._game, self._plot_dict)
        self._bullet_render.initialize(self._env, self._game, self._plot_dict)
        for render in self._custom_renders: render.initialize(self._env, self._game, self._plot_dict)



    def __call__(self, *args, **kwargs):
        self._map_render(self._env, self._game)
        self._npc_render(self._env, self._game)
        self._player_render(self._env, self._game)
        self._bullet_render(self._env, self._game)
        for render in self._custom_renders: render(self._env, self._game)
        push_notebook()



    @property
    def env(self): return self._env


    @property
    def game(self): return self._game








