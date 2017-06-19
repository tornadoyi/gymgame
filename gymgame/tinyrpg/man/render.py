# -*- coding: utf-8 -*-
from bokeh.io import output_notebook, show, push_notebook
from bokeh.plotting import figure
from bokeh.layouts import gridplot
import numpy as np
import random
import time

# ! only used to temporarily shutdown bokeh warning !
import warnings
warnings.filterwarnings('ignore')

# TODO: solve warning below
# \site-packages\bokeh\models\sources.py:89: BokehUserWarning: ColumnDataSource's columns must be of the same length
#  lambda: warnings.warn("ColumnDataSource's columns must be of the same length", BokehUserWarning))


class Render(object):
    """A game dashboard to show the game state"""
    def __init__(self, env):
        self._env = env
        self._game = env.game
        self._map = self._game.map

        # create figure
        bounds = self._map.bounds

        output_notebook()
        self._plt_map = figure(
            plot_width=600,
            plot_height=600,
            toolbar_location=None,
            x_range=(int(bounds.min.x), int(bounds.max.x)),
            y_range=(int(bounds.min.y), int(bounds.max.y)),
            # x_range=(min_screen_x - 1, max_screen_x + 1),
            # y_range=(max_screen_y + 1, min_screen_y - 1),
            x_axis_location="above",
            title="step #0"
        )

        self._plt_map.title.align = "center"
        self._plt_map.title.text_color = "orange"
        self._plt_map.title.text_font_size = "25px"
        self._plt_map.title.background_fill_color = "blue"

        self.player_num, self.npc_num = len(self._map.players), len(self._map.npcs)
        self.total_num = self.player_num + self.npc_num

        self.rd_loc = self._plt_map.circle(
            [-1] * self.total_num, [-1] * self.total_num,
            size=[50] * self.player_num + [20] * self.npc_num,
            line_color="gold",
            line_width=[10] * self.player_num + [1] * self.npc_num,
            fill_color=["green"] * self.player_num + ["yellow"] * self.npc_num,
            fill_alpha=0.6)

        # 显示reward趋势
        plt_reward = figure(
            plot_width=400, plot_height=400, title="running ep reward: ")
        plt_reward.title.align = "center"
        plt_reward.title.text_color = "green"
        plt_reward.title.text_font_size = "20px"
        plt_reward.title.background_fill_color = "black"
        self.plt_reward = plt_reward  # 用于后续更新标题中的reward值
        self.rd_reward = plt_reward.line(
            [1], [0], line_width=2)

        # put all the plots in a gridplot
        plt_combo = gridplot(
            [[self._plt_map, plt_reward]],
            # toolbar_location=None
        )

        # show the results
        self.nb_handle = show(plt_combo, notebook_handle=True)



    def update(self):
        """update bokeh plots according to new env state and action data"""
        # global_ob, reward, episode_count, current_step, current_is_caught = env_state_action

        # self._plt_map.title.text = "step: #{}".format(current_step)

        # note： 如果频率过快， jupyter notebook会受不了
        all_x = [_.attributes.position.x for _ in self.map.players] + [_.attributes.position.x for _ in self.map.npcs]
        all_y = [_.attributes.position.y for _ in self.map.players] + [_.attributes.position.y for _ in self.map.npcs]
        self.rd_loc.data_source.data['x'] = all_x
        self.rd_loc.data_source.data['y'] = all_y

        # 游戏结束时进行闪动， 表示游戏结束
        # thief_color = "red" if current_is_caught else "yellow"
        # self.rd_loc.data_source.data['fill_color'] = ["green"] * self.player_num + [thief_color] * self.npc_num
        # thief_lw = 3 if current_is_caught else 1
        # self.rd_loc.data_source.data['line_width'] = [10] * self.player_num + [thief_lw] * self.npc_num

        # self.rd_reward.data_source.data['x'] = range(len(reward))
        # self.rd_reward.data_source.data['y'] = reward
        # self.plt_reward.title.text = "episode #{} / last_ep_reward: {:5.1f}".format(
        #     episode_count, reward[-1] if reward else 0)
        push_notebook()  # self.nb_handle

