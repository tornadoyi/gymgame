from easydict import EasyDict as edict


class Renderer(object):
    def __init__(self, game):
        self._game = game


    @property
    def game(self): return self._game


    def __call__(self, *args, **kwargs): raise NotImplementedError('__call__ should be implemented')



class BokehRenderer(Renderer):

    def __init__(self, game, mode="notebook"):
        """bokeh_mode: notebook/bokeh_serve (need firstly run `bokeh serve`)"""

        super(BokehRenderer, self).__init__(game)
        self._mode = mode

        from bokeh.io import output_notebook, show, push_notebook
        from bokeh.client import push_session
        from bokeh.plotting import curdoc
        from bokeh.layouts import gridplot

        self._bokeh = edict(
            output_notebook = output_notebook,
            show = show,
            push_notebook = push_notebook,
            push_session = push_session,
            curdoc = curdoc,
            gridplot = gridplot,
        )

        if self._mode == 'notebook': output_notebook()

    @property
    def mode(self): return self._mode


    def __call__(self, *args, **kwargs):
        if self._mode == "notebook":
            self._bokeh.push_notebook()


    def _show(self, plots):
        plot = self._grid_plots(plots) if isinstance(plots, (list, tuple)) else plots

        # show the results
        if self._mode == "notebook":
            self._bokeh.show(plot, notebook_handle=True)
        else:
            session = self._bokeh.push_session(self._bokeh.curdoc())
            session.show(plot)


    def _grid_plots(self, plots):
        if len(plots) == 1: return plots[0]
        return self._bokeh.gridplot([plots])