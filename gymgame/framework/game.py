

_FPS = 60

class Game(object):
    def __init__(self, speed_scale=1.0):
        self._speed_scale = speed_scale
        self._total_steps = 0


        # runtime
        self._terminal = None
        self._steps = 0


    @property
    def total_steps(self): return self._total_steps

    @property
    def steps(self): return self._steps

    @property
    def terminal(self): return self._terminal

    @property
    def delta_time(self): return 1.0 / _FPS * self._speed_scale

    @property
    def speed_scale(self): return self._speed_scale

    @speed_scale.setter
    def speed_scale(self, v): self._speed_scale = v


    # virtual methods
    def _reset(self, *args, **kwargs): raise NotImplementedError("_reset should be implemented")

    def _step(self, *args, **kwargs): raise NotImplementedError("_step should be implemented")

    def _close(self, *args, **kwargs): raise NotImplementedError("_close should be implemented")

    def _render(self, *args, **kwargs): raise NotImplementedError("_renders should be implemented")

    def _check_terminal(self): raise NotImplementedError("_check_terminal should be implemented")


    def reset(self, *args, **kwargs):
        self._steps = 0
        self._terminal = False
        self._reset()


    def step(self, *args, **kwargs):
        if self._terminal == True: raise Exception("can not call step when game has been over")
        self._step(*args, **kwargs)
        self._terminal = self._check_terminal()
        self._steps += 1
        self._total_steps += 1


    def close(self, *args, **kwargs): self._close(*args, **kwargs)


    def render(self, *args, **kwargs): self._render(*args, **kwargs)