

class _Timer(object):
    def __init__(self, endtime, callback, *args, **kwargs):
        self.endtime = endtime
        self.callback = callback
        self.args = args
        self.kwargs = kwargs


    def __call__(self): self.callback(*self.args, **self.kwargs)


class Scheduler(object):
    def __init__(self):
        self._timers = []
        self._time = 0


    @property
    def time(self): return self._time


    # virtual
    def _update(self): pass


    def update(self, time):
        self._time = time
        self._update()

        # check timers
        timers = self._timers
        count = 0
        for i in range(len(timers)):
            t = timers[i]
            if t.endtime < self._time:
                count += 1
            else:
                break
        if count == 0: return

        # call timer
        self._timers = timers[count :]
        for i in range(count):
            timers[i]()


    def schedule(self, delay, f, *args, **kwargs):
        endtime = self._time + delay
        t = _Timer(endtime, f, *args, **kwargs)

        if len(self._timers) == 0:
            self._timers.append(t)
            return

        # binary search
        timers = self._timers
        st = 0
        ed = len(timers)
        while st < ed:
            md = int(st + ed) >> 1
            v = timers[md]
            if v.endtime > t.endtime: ed = md - 1
            elif v.endtime < t.endtime: st = md + 1

        timers.insert(st, t)



    def unschedule(self, f):
        index = None
        for i in range(len(self._timers)):
            if f != self._timers[i].callback: continue
            index = i

        if index is None: return None
        return self._timers.pop(index)


    def unschedule_all(self): self._timers = []
