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
    def initialize(self, env, game, plot_dict):
        # TODO: 注意!! bokeh有点bug, 有可能初始化后的子弹数, 更新时只能显示最多那么多子弹了, 也就是说初始化时是上限
        c_list = game.map.characters
        c_num = len(c_list)

        # 暂时用fill_alpha来表示血量的状况
        self.rd = plot_dict.map.circle(
            [-1] * c_num, [-1] * c_num,
            radius=[_.attribute.radius for _ in c_list],
            line_color=[self._get_line_color(_) for _ in c_list],
            line_width=[1] * c_num,
            fill_color=["firebrick"] * c_num,
            fill_alpha=[_c.attribute.hp/_c.attribute.max_hp for _c in c_list]
        )

    def _get_line_color(self, character):
        return "red"

    def __call__(self, env, game):
        c_list = game.map.characters
        all_x = [_.attribute.position.x for _ in c_list]
        all_y = [_.attribute.position.y for _ in c_list]
        self.rd.data_source.data['x'] = all_x
        self.rd.data_source.data['y'] = all_y


class NPCRender(CharacterRender):
    pass


class PlayerRender(CharacterRender):
    pass


class BulletRender(ObjectRender):
    def initialize(self, env, game, plot_dict):
        # TODO: 注意!! bokeh有点bug, 有可能初始化后的子弹数, 更新时只能显示最多那么多子弹了, 也就是说初始化时是上限
        bullet_num = len(game.map.bullets)
        self.rd_bullets = plot_dict.map.circle(
            [-1] * bullet_num, [-1] * bullet_num,
            radius=[_.attribute.radius for _ in game.map.bullets],
            line_color="red",
            # line_width=[1] * bullet_num,
            # fill_color=["firebrick"] * bullet_num,
            # fill_alpha=0.6
        )

    def __call__(self, env, game):
        all_x = [_.attribute.position.x for _ in game.map.bullets]
        all_y = [_.attribute.position.y for _ in game.map.bullets]
        self.rd_bullets.data_source.data['x'] = all_x
        self.rd_bullets.data_source.data['y'] = all_y



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

        show(self._plot_dict.map, notebook_handle=True)


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








