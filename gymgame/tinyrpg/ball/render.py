from bokeh.io import output_notebook, show, push_notebook
from bokeh.plotting import figure
from bokeh.layouts import gridplot


class Render(object):
    def __init__(self, env):
        self._env = env
        self._game = env.game
        self._map = self._game.map

        # create figure
        bounds = self._map.bounds
        output_notebook()
        self._plt_map = figure(
            plot_width=int(bounds.size.x),
            plot_height=int(bounds.size.y),
            toolbar_location=None,
            x_range=(int(bounds.min.x), int(bounds.max.x)),
            y_range=(int(bounds.min.y), int(bounds.max.y)),
        )


    def update(self):
        pass