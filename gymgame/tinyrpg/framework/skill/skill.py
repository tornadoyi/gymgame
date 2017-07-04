import numpy as np
from ..config import Relation



class Skill(object):
    def __init__(self,
                 id,
                 cast_time = 0,
                 cd_time = 0,
                 mp_cost = 0,
                 target_required = False,
                 target_relation = Relation.any,
                 cast_distance = np.inf,
                 bullet_emitter = None,
                 self_factors = [],
                 target_factors = [],
                 ):

        self._id = id
        self._cast_time = cast_time
        self._cd_time = cd_time
        self._mp_cost = mp_cost
        self._target_required = target_required
        self._target_relation = target_relation
        self._cast_distance = cast_distance
        self._bullet_emitter = bullet_emitter
        self._self_factors = self_factors
        self._target_factors = target_factors


        # runtime
        self.last_cast_time = 0



    def __repr__(self): return self.__str__()


    def __str__(self): return "{0}".format(self._id)


    @property
    def id(self): return self._id

    @property
    def cast_time(self): return self._cast_time

    @property
    def cd_time(self): return self._cd_time

    @property
    def mp_cost(self): return self._mp_cost

    @property
    def target_required(self): return self._target_required

    @property
    def target_relation(self): return self._target_relation

    @property
    def cast_distance(self): return self._cast_distance

    @property
    def bullet_emitter(self): return self._bullet_emitter

    @property
    def self_factors(self): return self._self_factors

    @property
    def target_factors(self): return self._target_factors



    def set_bullet_hit_callback(self, callback):
        if self._bullet_emitter is None: return
        self._bullet_emitter.hit_callback = callback




class SkillManager(object):
    def __init__(self, master, skills):
        self._master = master
        self._skill_dict = {}
        self._skill_list = []

        # learn skills
        for skill in skills:
            if skill.id in self._skill_dict: raise Exception('repeated skill {0} can not be learned'.format(skill.id))
            # set bullet hit callback
            skill.set_bullet_hit_callback(self._do_factors)

            # save
            self._skill_dict[skill.id] = skill
            self._skill_list.append(skill)


        # runtime
        self._casting_skill = None
        self._updater = None


    @property
    def skill_list(self): return self._skill_list


    @property
    def casting(self): return self._casting_skill


    @property
    def busy(self): return self._check_busy()


    @property
    def master(self): return self._master


    @property
    def game(self): return self._master.game


    def update(self):
        if not self.busy: return False
        if self._updater is not None: self._updater(self._master)
        return True




    def can_cast(self, skill, target=None, position=None):
        # check casting
        if self.casting: return False

        # get skill
        skill = self._skill(skill)

        # cd check
        if not self._check_cd(skill): return False

        # cost check
        if not self._check_cost(skill): return False

        # distance check
        if not self._check_distance(skill, target, position): return False

        # target check
        if not self._check_target(skill, target): return False

        return True



    def stop_all(self):
        self.stop_cast()
        self.stop_updater()


    def stop_cast(self):
        if self._casting_skill is None: return
        self._master.unschedule(self._cast_end)
        self._casting_skill = None


    def stop_updater(self):
        self._master.unschedule(self._updater)
        self._updater = None



    def cast(self, skill, target=None, position=None):
        # check
        skill = self._skill(skill)
        if not self.can_cast(skill, target, position): return False

        # set last cast time
        skill.last_cast_time = self.game.time

        # cost mp
        self._master.attribute.mp -= skill.mp_cost

        # set direct
        if target is not None or position is not None:
            target_position = target.attribute.position if position is None else position
            self._master.attribute.direct = (target_position - self._master.attribute.position).normalized

        # start cast
        self._cast_start(skill, target, position)

        return True



    def _cast_start(self, skill, target=None, position=None):
        self._casting_skill = skill
        if skill.cast_time == 0:
            self._cast_end(target, position)

        else:
            self._master.schedule(skill.cast_time, self._cast_end, target, position)



    def _cast_end(self, target=None, position=None):
        skill = self._casting_skill
        self._casting_skill = None
        self._do_effect(skill, target, position)



    def _do_effect(self, skill, target=None, position=None):
        # check
        if not self._check_target(skill, target): return
        if not self._check_distance(skill, target, position): return

        # bullet
        if skill.bullet_emitter: skill.bullet_emitter(self._master)

        # self factors
        for factor in skill.self_factors: factor(self._master, self._master)

        # target factors
        for factor in skill.target_factors: factor(self._master, target)




    def _do_factors(self, factors, target):
        count = 0
        for factor in factors:
            if not self._master.is_relation(factor.relation, target): continue
            factor(self._master, target)
            count += 1

        return count > 0 # bullet emitter used



    def _check_busy(self): return (self._casting_skill is not None or self._updater is not None)


    def _check_cost(self, skill): return self._master.attribute.mp >= skill.mp_cost


    def _check_cd(self, skill): return (self._master.game.time - skill.last_cast_time) > skill.cd_time


    def _check_target(self, skill, target):
        if not skill.target_required: return True
        if target is None: return False

        # relation
        return self._master.is_relation(skill.target_relation, target)


    def _check_distance(self, skill, target, position):
        # distance
        if skill.cast_distance == np.inf: return True
        p = position if target is None else target.attribute.position
        if p is None: return False
        if self._master.attribute.position.distance(p) > skill.cast_distance: return False
        return True


    def _skill(self, skill): return skill if isinstance(skill, Skill) else self._skill_dict[skill]







