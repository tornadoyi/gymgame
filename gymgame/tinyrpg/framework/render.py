import numpy as np
from easydict import EasyDict as edict
from bokeh.plotting import figure, curdoc
from bokeh.layouts import gridplot
from gymgame.tinyrpg.framework import config
import colorsys
import warnings
from gymgame import framework
warnings.filterwarnings('ignore')

# https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F
CAMP_COLORS = ["#568203", "#003A6C", "#e32636", "#efdecd", "#e52b50", "#ffbf00", "#ff033e",
               "#9966cc", "#a4c639", "#f2f3f4", "#cd9575", "#915c83", "#faebd7", "#008000",
               "#8db600", "#fbceb1", "#00ffff", "#7fffd4", "#4b5320", "#e9d66b", "#b2beb5",
               "#87a96b", "#ff9966", "#a52a2a", "#fdee00", "#6e7f80", "#ff2052", "#007fff",
               "#f0ffff", "#89cff0", "#a1caf1", "#f4c2c2"]

CAMP_COLORS = {_c: CAMP_COLORS[_i]
               for _i, _c in enumerate(config.Camp)}

class ModuleRenderer():

    def __call__(self): pass

    def initialize(self, render_state):
        self.render_state = render_state
        self.game = render_state.game


class NoneRenderer(ModuleRenderer): pass


class ObjectRenderer(ModuleRenderer): pass


class CharacterRenderer(ObjectRenderer):
    def initialize(self, *args, **kwargs):
        super(CharacterRenderer, self).initialize(*args, **kwargs)
        c_list = self._get_characters()
        c_num = len(c_list)

        self.rd = self.render_state.map.circle(
            [-1] * c_num, [-1] * c_num,
            radius=[_.attribute.radius for _ in c_list],
            line_color=[self._get_line_color(_) for _ in c_list],
            line_width=[3] * c_num,
            fill_color=["firebrick"] * c_num,
            fill_alpha=[_c.attribute.hp/_c.attribute.max_hp for _c in c_list]
        )

        self.rd_direct = self.render_state.map.multi_line(xs=[], ys=[], line_color=[], line_width=[])

    def _get_line_color(self, character):
        # for multi-camp, use this: [(a >> i) & 1 for i in range(32)]
        # now we only consider single camp situation
        return CAMP_COLORS[character.attribute.camp]

    def __call__(self, *args, **kwargs):
        c_list = self._get_characters()
        all_x = [_.attribute.position.x for _ in c_list]
        all_y = [_.attribute.position.y for _ in c_list]
        self.rd.data_source.data['x'] = all_x
        self.rd.data_source.data['y'] = all_y
        self.rd.data_source.data['radius'] = [_.attribute.radius for _ in c_list]

        # 暂时用fill_alpha来表示血量的状况
        self.rd.data_source.data['fill_alpha'] = [_c.attribute.hp / _c.attribute.max_hp for _c in c_list]

        direct_x, direct_y = [], []
        for o in c_list:
            src = o.attribute.position
            dst = o.attribute.position + o.attribute.direct * o.attribute.radius * 1.5
            direct_x.append([src.x, dst.x])
            direct_y.append([src.y, dst.y])

        self.rd_direct.data_source.data['xs'] = direct_x
        self.rd_direct.data_source.data['ys'] = direct_y
        self.rd_direct.data_source.data['line_color'] = ['black'] * len(c_list)
        self.rd_direct.data_source.data['line_width'] = [2] * len(c_list)


    def _get_characters(self): raise NotImplementedError('_get_characters should be impolemented')


class NPCRenderer(CharacterRenderer):
    def _get_characters(self): return self.game.map.npcs



class PlayerRenderer(CharacterRenderer):
    def _get_characters(self): return self.game.map.players



class BulletRenderer(ObjectRenderer):
    def initialize(self, *args, **kwargs):
        super(BulletRenderer, self).initialize(*args, **kwargs)
        bullet_num = len(self.game.map.bullets)
        self.rd_bullets = self.render_state.map.circle(
            [-1] * bullet_num, [-1] * bullet_num,
            radius=[_.attribute.radius for _ in self.game.map.bullets],
            line_color="red",
            fill_color="purple",
            fill_alpha=0.6
            # line_width=[1] * bullet_num,
            # fill_color=["firebrick"] * bullet_num,
            # fill_alpha=0.6
        )

    def __call__(self):
        all_x = [_.attribute.position.x for _ in self.game.map.bullets]
        all_y = [_.attribute.position.y for _ in self.game.map.bullets]
        self.rd_bullets.data_source.data['x'] = all_x
        self.rd_bullets.data_source.data['y'] = all_y
        # 注意!! radius 必须设置上, 否则如果初始化时radius为空, 则后续再也无法显示出来了
        self.rd_bullets.data_source.data['radius'] = [_.attribute.radius for _ in self.game.map.bullets]


class MapRenderer(ModuleRenderer):
    def __init__(self, witdh=600, height=600):
        self._with = witdh
        self._height = height

    @property
    def plot_map(self): return self._plt_map


    def initialize(self, *args, **kwargs):
        super(MapRenderer, self).initialize(*args, **kwargs)
        map = self.game.map
        # create figure
        bounds = map.bounds
        _x_min, _x_max = int(bounds.min.x), int(bounds.max.x)
        _y_min, _y_max = int(bounds.min.y), int(bounds.max.y)
        _x_size = _x_max - _x_min
        _y_size = _y_max - _y_min

        self._plt_map = figure(
            plot_width=self._with,
            plot_height=self._height,
            x_range=(_x_min - _x_size * 0.1, _x_max + _x_size * 0.1),
            y_range=(_y_min - _y_size * 0.1, _y_max + _y_size * 0.1),
        )

        # draw edge
        self._plt_map.line(x=[_x_min, _x_max, _x_max, _x_min, _x_min],
                           y=[_y_min, _y_min, _y_max, _y_max, _y_min],
                           line_color="navy", line_alpha=0.3, line_dash="dotted", line_width=2)

        self.render_state.map = self._plt_map
        return self._plt_map







class Renderer(framework.BokehRenderer):
    def __init__(self, game, mode="notebook",
                 map_render=None, npc_render=None, player_render=None, bullet_render=None,
                 ):
        """bokeh_mode: notebook/bokeh_serve(need firstly run `bokeh serve`)"""

        super(Renderer, self).__init__(game, mode)
        self._map_render = map_render or MapRenderer()
        self._npc_render = npc_render or NPCRenderer()
        self._player_render = player_render or PlayerRenderer()
        self._bullet_render = bullet_render or BulletRenderer()
        self._custom_renders = self._custom_renderers()
        self._renders = [self._map_render, self._npc_render, self._player_render, self._bullet_render] + self._custom_renders
        self._render_state = edict(game=game)


        # initialize
        plots = []
        for r in self._renders:
            plot = r.initialize(self._render_state)
            if plot is None: continue
            plots.append(plot)

        # show the results
        self._show(plots)


    def __call__(self, *args, **kwargs):
        for r in self._renders: r()
        super(Renderer, self).__call__()



    def _custom_renderers(self): return []






