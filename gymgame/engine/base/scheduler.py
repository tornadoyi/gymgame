

class _Timer(object):
    def __init__(self, delay, repeated, callback, *args, **kwargs):
        self.delay = delay
        self.repeated = repeated
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.startime = None
        self.endtime = None


    def __call__(self): self.callback(*self.args, **self.kwargs)


    def refresh(self, starttime):
        self.startime = starttime
        self.endtime = starttime + self.delay



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
            t = timers[i]
            t()
            if not t.repeated: continue
            self._save_timer(t)



    def schedule(self, delay, f, *args, **kwargs):
        t = _Timer(delay, True, f, *args, **kwargs)
        self._save_timer(t)


    def schedule_once(self, delay, f, *args, **kwargs):
        t = _Timer(delay, False, f, *args, **kwargs)
        self._save_timer(t)



    def unschedule(self, f):
        index = None
        for i in range(len(self._timers)):
            if f != self._timers[i].callback: continue
            index = i

        if index is None: return None
        return self._timers.pop(index)


    def unschedule_all(self): self._timers = []


    def _save_timer(self, t):
        t.refresh(self._time)
        timers = self._timers

        if len(timers) == 0:
            timers.append(t)
            return

        # binary search
        st = 0
        ed = len(timers)
        while st < ed:
            md = int(st + ed) >> 1
            v = timers[md]
            if v.endtime > t.endtime:
                ed = md - 1
            else:
                st = md + 1

        timers.insert(st, t)
