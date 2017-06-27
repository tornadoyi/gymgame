import numpy as np
from easydict import EasyDict as edict
from .object import Object
from ..config import Attr


class Bullet(Object):

    def __init__(self, data, hit_callback, end_callback):
        super(Bullet, self).__init__(data)

        self._hit_callback = hit_callback
        self._end_callback = end_callback

        #runtime
        self._start_time, self._end_time, self._expect_end_time = None, None, None
        self._start_position, self._end_position = None, None



    def move_toward(self, direct, speed=None): self._map.move_toward(self.attribute.id, direct, speed, bounds_limit=False)

    def move_to(self, position): self._map.move_to(self.attribute.id, position, bounds_limit=False)


    def enter_map(self, map):
        super(Bullet, self).enter_map(map)

        self._attribute.hp = self._attribute.max_hp
        self._start_time = map.game.time
        self._end_time = None
        self._expect_end_time = self._start_time + self._atrribute.max_range / self._attribute.speed
        self._start_position = self._attribute.position
        self._end_position = None


    def exit_map(self):
        self._end_time = self.game.time
        self._end_position = self.attribute.position
        super(Bullet, self).exit_map()
        if self._end_callback: self._end_callback(self)



    def on_hit(self, target):
        if not self._hit_callback(target): return

        # hit one
        self.attribute.hp -= 1
        if self.attribute.hp > 0: return

        # end of trip
        self.map.remove(self.attribute.id)



    def _update(self):
        if self.game.time < self._expect_end_time:
            self.move_toward(self.attribute.direct)

        else:
            # end of trip
            self.map.remove(self.attribute.id)



    def _init_attribute(self):
        super(Bullet, self)._init_attribute()
        self._add_attr('static', Attr.max_range)
        self._add_attr('plus', Attr.max_hp, base=0.0, range=(0, np.inf))
        self._add_attr('value', Attr.hp, base=self._attribute.max_hp, range=(0, lambda: self._attribute.max_hp))




class Emitter():
    def __init__(self, count, speed, penetration=1, max_range=1.0, radius=0.1, factors=[]):
        self._bullet_count = count
        self._bullet_speed = speed
        self._penetration  = penetration
        self._max_range = max_range
        self._radius = radius
        self._factors = factors

        # run time
        self._gen_bullet_count = 0
        self._bullet_cache = []
        self._hit_callback = None


    def __call__(self, master):
        bullets = self._get_bullets()
        self._deploy_bullets(master, bullets)
        for bullet in bullets: master.map.add(bullet)


    @property
    def hit_callback(self): return self._hit_callback


    @hit_callback.setter
    def hit_callback(self, v): self._hit_callback = v


    def _deploy_bullets(self, master, bullets): raise NotImplementedError('_deploy_bullets need to be implemented')


    def _get_bullets(self):

        def _create():
            id = 'bullet-{0}'.format(self._gen_bullet_count)
            self._gen_bullet_count += 1
            return Bullet(edict(id=id,
                                max_hp=self._penetration,
                                speed=self._bullet_speed,
                                max_range=self._max_range,
                                radius = self._radius
                                ),
                          hit_callback=lambda target: self._hit_callback(self._factors, target),
                          end_callback=lambda bullet: self._bullet_cache.append(bullet)
                          )

        # reload
        need_count = self._bullet_count - len(self._bullet_cache)
        for i in range(need_count): self._bullet_cache.append(_create())

        # get sleep bullets
        bullets = self._bullet_cache[0:self._bullet_count]
        self._bullet_cache = self._bullet_cache[self._bullet_count :]
        return bullets




class SingleEmitter(Emitter):
    
    def __init__(self, *args, **kwargs):
        super(SingleEmitter, self).__init__(1, *args, **kwargs)


    def _deploy_bullets(self, master, bullets):
        direct = master.attribute.direct
        position = master.attribute.position + direct * master.attribute.radius * 1.1

        for bullet in bullets:
            bullet.position = position
            bullet.direct = direct
    


class CircleEmitter(Emitter):

    def _deploy_bullets(self, master, bullets):
        d = master.attribute.direct
        r = master.attribute.radius * 1.1
        p = master.attribute.position
        a = 360.0 / len(bullets)


        for i in range(len(bullets)):
            bullet = bullets[i]
            d = d.rotate(a).normalized
            bullet.direct = d
            bullet.position = p + d * r

