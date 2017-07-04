import numpy as np
from ..framework.config import Relation
from . import config

class AI(object):
    def __init__(self, master):
        self._master = master
        self._skill = master.skill

        self._enemy_skills = []
        self._friend_skills = []

        self._analyse_skills()



    def __call__(self):
        # choose target
        enemy = self._get_nearest_enemy()
        friend_skills, enemy_skills = self._get_valid_skills(enemy)


        # move
        if len(friend_skills) + len(enemy_skills) == 0:
            self._master.move_to(enemy.attribute.position)
            return True


        # choose skill
        skill = None
        target = None
        if len(friend_skills) > 0 and np.random.rand() < config.AI.defense_probability:
            skill = friend_skills[np.random.randint(0, len(friend_skills))]
            target = self._master
        else:
            skill = enemy_skills[np.random.randint(0, len(enemy_skills))]
            target = enemy

        self._master.cast_skill(skill, target)

        return True



    def _get_nearest_enemy(self):
        enemies = [char for char in self._master.map.characters if self._master.is_enemy(char)]
        if len(enemies) == 0: return None
        if len(enemies) == 1: return enemies[0]

        distance = np.inf
        target = None
        for enemy in enemies:
            d = self._master.attribute.position.distance(enemy.attribute.position)
            if d > distance: continue
            distance = d
            target = enemy

        return enemy


    def _get_valid_skills(self, enemy):

        valid_enemy_skills = []
        for skill in self._enemy_skills:
            if not self._skill.can_cast(skill, enemy): continue
            valid_enemy_skills.append(skill)

        valid_friend_skills = []
        for skill in self._friend_skills:
            if not self._skill.can_cast(skill, enemy): continue
            valid_friend_skills.append(skill)

        return valid_friend_skills, valid_enemy_skills


    def _analyse_skills(self):

        def _analyse(skill):
            friend = enemy = None
            if skill.target_required:
                if skill.target_relation == Relation.friend:
                    friend = True
                elif skill.target_relation == Relation.enemy:
                    enemy = True
                else:
                    friend = enemy = True

            if len(skill.self_factors) > 0: friend = True

            if skill.bullet_emitter is not None:
                for f in skill.bullet_emitter.factors:
                    if f.relation == Relation.friend:
                        friend = True
                    elif f.relation == Relation.enemy:
                        enemy = True
                    else:
                        friend = enemy = True

            return friend, enemy


        skills = self._skill.skill_list

        for skill in skills:
            friend, enemy = _analyse(skill)
            if friend: self._friend_skills.append(skill)
            if enemy: self._enemy_skills.append(skill)

