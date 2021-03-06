# -*- coding: utf-8 -*-
import numpy as np
import random
import time
from bokeh.io import output_notebook, show, push_notebook
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from .. import framework

# ! only used to temporarily shutdown bokeh warning !
import warnings
warnings.filterwarnings('ignore')

# TODO: solve warning below
# \site-packages\bokeh\models\sources.py:89: BokehUserWarning: ColumnDataSource's columns must be of the same length
#  lambda: warnings.warn("ColumnDataSource's columns must be of the same length", BokehUserWarning))


class Renderer(framework.Renderer):
    """A game dashboard to show the game state"""
    def __init__(self, game):
        #super(Render, self).__init__(*args, **kwargs)
        self._game = game
        self._map = self._game.map
        self.global_running_r = []

        # create figure
        bounds = self._map.bounds
        _x_min, _x_max = int(bounds.min.x), int(bounds.max.x)
        _y_min, _y_max = int(bounds.min.y), int(bounds.max.y)
        _x_size = _x_max - _x_min
        _y_size = _y_max - _y_min

        output_notebook()

        self._plt_map = figure(
            plot_width=600,
            plot_height=600,
            # toolbar_location=None,
            x_range=(_x_min - _x_size*0.1, _x_max + _x_size*0.1),
            y_range=(_y_min - _y_size*0.1, _y_max + _y_size*0.1),
            # x_range=(min_screen_x - 1, max_screen_x + 1),
            # y_range=(max_screen_y + 1, min_screen_y - 1),
            x_axis_location="above",
            title="step #0"
        )

        self._plt_map.title.align = "center"
        self._plt_map.title.text_color = "orange"
        self._plt_map.title.text_font_size = "25px"
        self._plt_map.title.background_fill_color = "blue"

        # draw edge
        self._plt_map.line(x=[_x_min, _x_max, _x_max, _x_min, _x_min], y=[_y_min, _y_min, _y_max, _y_max, _y_min],
                           line_color="navy", line_alpha=0.3, line_dash="dotted", line_width=2)

        self.player_num, self.bullet_num, self.coin_num = \
            len(self._map.players), len(self._map.bullets), len(self._map.coins)
        self.total_num = self.player_num + self.bullet_num + self.coin_num

        # draw balls
        self.rd_loc = self._plt_map.circle(
            [-1] * self.total_num, [-1] * self.total_num,
            radius=[_.attribute.radius for _ in self._map.players]
                   + [_.attribute.radius for _ in self._map.bullets]
                   + [_.attribute.radius for _ in self._map.coins],
            line_color="gold",
            line_width=[2] * self.player_num + [1] * self.bullet_num + [1] * self.coin_num,
            fill_color=["green"] * self.player_num + ["firebrick"] * self.bullet_num + ["blue"] * self.coin_num,
            fill_alpha=0.6)

        # show reward trend
        plt_reward = figure(
            plot_width=400, plot_height=400, title="running ep reward: ")
        plt_reward.title.align = "center"
        plt_reward.title.text_color = "green"
        plt_reward.title.text_font_size = "20px"
        plt_reward.title.background_fill_color = "black"
        self.plt_reward = plt_reward  # used for update reward in title
        self.rd_reward = plt_reward.line(
            [1], [0], line_width=2)

        # put all the plots in a gridplot
        plt_combo = gridplot(
            [[self._plt_map, plt_reward]],
            # toolbar_location=None
        )

        # show the results
        self.nb_handle = show(plt_combo, notebook_handle=True)



    def __call__(self, *args, **kwargs):
        """update bokeh plots according to new env state and action data"""

        # self._plt_map.title.text = "step: #{}".format(current_step)
        self._plt_map.title.text = "step: #{}".format(self._game.steps)

        # note： 如果频率过快， jupyter notebook会受不了
        self._map = self._game.map
        all_x = [_.attribute.position.x for _ in self._map.players] \
                + [_.attribute.position.x for _ in self._map.bullets] \
                + [_.attribute.position.x for _ in self._map.coins]
        all_y = [_.attribute.position.y for _ in self._map.players] \
                + [_.attribute.position.y for _ in self._map.bullets] \
                + [_.attribute.position.y for _ in self._map.coins]
        self.rd_loc.data_source.data['x'] = all_x
        self.rd_loc.data_source.data['y'] = all_y


        # 游戏结束时进行闪动， 表示游戏结束
        # thief_color = "red" if current_is_caught else "yellow"
        # self.rd_loc.data_source.data['fill_color'] = ["green"] * self.player_num + [thief_color] * self.bullet_num
        # thief_lw = 3 if current_is_caught else 1
        # self.rd_loc.data_source.data['line_width'] = [10] * self.player_num + [thief_lw] * self.bullet_num

        # update training performance after each episode
        # close running reward
        # if self._game.terminal:
        #     ep_reward = sum(self._env.rewards)
        #     ep_count = len(self.global_running_r)
        #     if len(self.global_running_r) == 0:  # record running episode reward
        #         self.global_running_r.append(ep_reward)
        #     else:
        #         self.global_running_r.append(0.99 * self.global_running_r[-1] + 0.01 * ep_reward)
        #
        #     self.rd_reward.data_source.data['x'] = range(ep_count)
        #     self.rd_reward.data_source.data['y'] = self.global_running_r
        #     #self.plt_reward.title.text = "episode #{} / last_ep_reward: {:5.1f}".format(
        #       #  ep_count, self.global_running_r[-1])

        push_notebook()  # self.nb_handle
