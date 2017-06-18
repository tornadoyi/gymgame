

class Event(object):

    def __init__(self):
        self._event_dict = {}


    def __call__(self, *args, **kwargs): self.send_event(*args, **kwargs)


    def add_event(self, id, callback):
        assert id is not None
        assert callback is not None

        events = self._event_dict.get(id, [])
        events.append(callback)
        self._event_dict[id] = events



    def send_event(self, id, *args, **kwargs):
        events = self._event_dict.get(id, [])
        for e in events: e(*args, **kwargs)


