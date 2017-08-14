import numpy as np


class Game(object):
    def __init__(self, fps = 60, speed_scale=1.0, max_steps=np.inf):
        self._fps = fps
        self._speed_scale = speed_scale
        self._total_resets = 0
        self._total_steps = 0
        self._max_steps = max_steps
        self._renderer = None


        # runtime
        self._terminal = None
        self._steps = 0
        self._time = 0


    @property
    def total_resets(self): return self._total_resets

    @property
    def total_steps(self): return self._total_steps

    @property
    def steps(self): return self._steps

    @property
    def terminal(self): return self._terminal

    @property
    def time(self): return self._time

    @property
    def delta_time(self): return 1.0 / self._fps * self._speed_scale

    @property
    def speed_scale(self): return self._speed_scale

    @speed_scale.setter
    def speed_scale(self, v): self._speed_scale = v

    @property
    def fps(self): return self._fps

    @fps.setter
    def fps(self, v): self._fps = v

    @property
    def max_steps(self): return self._max_steps

    @property
    def renderer(self): return self._renderer

    @renderer.setter
    def renderer(self, v): self._renderer = v


    # virtual methods
    def _reset(self, *args, **kwargs): raise NotImplementedError("_reset should be implemented")

    def _step(self, *args, **kwargs): raise NotImplementedError("_step should be implemented")

    def _close(self, *args, **kwargs): raise NotImplementedError("_close should be implemented")

    def _render(self, *args, **kwargs):
        if self._renderer is None: raise NotImplementedError("no renderer for render")
        self._renderer()


    def _check_terminal(self): return self._steps >= self._max_steps - 1


    def reset(self, *args, **kwargs):
        self._total_resets += 1
        self._steps = 0
        self._time = 0
        self._terminal = False
        self._reset()


    def step(self, *args, **kwargs):
        if self._terminal == True: raise Exception("can not call step when game has been over")
        self._time += self.delta_time
        self._step(*args, **kwargs)
        self._terminal = self._check_terminal()
        self._steps += 1
        self._total_steps += 1



    def close(self, *args, **kwargs): self._close(*args, **kwargs)


    def render(self, *args, **kwargs): self._render(*args, **kwargs)