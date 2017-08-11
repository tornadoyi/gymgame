import numpy as np
from easydict import EasyDict as edict
from gymgame.engine import extension, Vector2
from gymgame.tinyrpg.sword import config, Serializer, EnvironmentGym
from gymgame.tinyrpg.framework import Skill, Damage, SingleEmitter
from gym import spaces



GAME_NAME = config.GAME_NAME

config.BOKEH_MODE = "bokeh_serve"  # you need run `bokeh serve` firstly

config.MAP_SIZE = Vector2(30, 30)

#config.GRID_SIZE = Vector2(20, 20)

config.GAME_PARAMS.fps = 24

config.GAME_PARAMS.max_steps = 300

config.NUM_PLAYERS = 1

config.NUM_NPC = 1

config.PLAYER_INIT_RADIUS = (0.0, 1.0)

config.NPC_INIT_RADIUS = (0.0, 1.0)

config.NPC_SKILL_COUNT = 1

config.SKILL_DICT = {
    'normal_attack' : Skill(
        id = 'normal_attack',
        cast_time = 0.0,#0.1,
        mp_cost = 0,
        target_required = True,
        target_relation = config.Relation.enemy,
        cast_distance = 1.0,
        target_factors = [Damage(200.0, config.Relation.enemy)]
    ),

    'normal_shoot' : Skill(
        id = 'normal_shoot',
        cast_time = 0.0, #0.3,
        mp_cost = 0,
        bullet_emitter = SingleEmitter(
            speed=0.3 * config.GAME_PARAMS.fps,
            penetration=1.0,
            max_range=config.MAP_SIZE.x * 0.8,
            radius=0.1,
            factors=[Damage(5.0, config.Relation.enemy)])
    ),

    'puncture_shoot' : Skill(
        id = 'normal_shoot',
        cast_time = 0.0,#0.3,
        mp_cost = 0,
        bullet_emitter = SingleEmitter(
            speed=0.3 * config.GAME_PARAMS.fps,
            penetration=np.Inf,
            max_range=config.MAP_SIZE.x * 0.8,
            radius=0.1,
            factors=[Damage(5.0, config.Relation.enemy)])
    ),
}

config.PLAYER_SKILL_LIST = [config.SKILL_DICT['puncture_shoot']]

config.NPC_SKILL_LIST = [config.SKILL_DICT['normal_attack']]


config.BASE_PLAYER = edict(
    id = "player-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 0.3 * config.GAME_PARAMS.fps,
    radius = 0.5,
    max_hp = 100.0,
    camp = config.Camp[0],
    skills=config.PLAYER_SKILL_LIST
)


config.BASE_NPC = edict(
    id = "npc-{0}",
    position = Vector2(0, 0),
    direct = Vector2(0, 0),
    speed = 0.1 * config.GAME_PARAMS.fps,
    radius = 0.5,
    max_hp = 400.0,
    camp = config.Camp[1],
    skills=config.NPC_SKILL_LIST
)





@extension(EnvironmentGym)
class EnvExtension():
    def _init_action_space(self): return spaces.Discrete(9)

    def _reset(self):
        s = super(EnvironmentGym, self)._reset()

        map = self.game.map
        player, npcs = map.players[0], map.npcs

        self.max_hp = max([player.attribute.hp] + [o.attribute.hp for o in npcs])
        self.pre_player_hp = player.attribute.hp
        self.pre_npc_hp = sum([o.attribute.hp for o in npcs])

        return s

    def _reward(self):
        map = self.game.map
        player, npcs = map.players[0], map.npcs


        # if player.attribute.hp < 1e-6: return -1
        # elif len(npcs) == 0: return 1
        # else: return 0



        if player.attribute.hp < 1e-6: return -1

        sub_player_hp = player.attribute.hp - self.pre_player_hp
        npc_hp = 0 if len(npcs) == 0 else sum([o.attribute.hp for o in npcs])
        sub_npc_hp = npc_hp - self.pre_npc_hp

        self.pre_player_hp = player.attribute.hp
        self.pre_npc_hp = npc_hp

        r = (sub_player_hp - sub_npc_hp) / self.max_hp

        if len(npcs) == 0: r += player.attribute.hp / self.max_hp

        return r




@extension(Serializer)
class SerializerExtension():

    DIRECTS = [Vector2.up,
               Vector2.up + Vector2.right,
               Vector2.right,
               Vector2.right + Vector2.down,
               Vector2.down,
               Vector2.down + Vector2.left,
               Vector2.left,
               Vector2.left + Vector2.up,
               ]


    def _deserialize_action(self, data):
        index, target = data
        if index < 8:
            direct = SerializerExtension.DIRECTS[index]
            actions = [('player-0', config.Action.move_toward, direct, None)]

        else:
            skill_index = index - 8
            skill_id = config.BASE_PLAYER.skills[skill_index].id
            actions = [('player-0', config.Action.cast_skill, skill_id, target, None)]

        return actions



    def _serialize_map(self, k, map):
        s_players = k.do_object(map.players, self._serialize_player)
        s_npcs = k.do_object(map.npcs, self._serialize_npc)
        s_bullets = []#k.do_object(map.bullets, self._serialize_bullet)

        if self._grid_size is None:
            return np.hstack([s_players, s_npcs, s_bullets])

        else:
            bounds = map.bounds
            grid_players = self._objects_to_grid(bounds, map.players, s_players, self._player_shape)
            grid_npcs = self._objects_to_grid(bounds, map.npcs, s_npcs, self._npc_shape)
            grid_bullets = None#self._objects_to_grid(bounds, map.bullets, s_bullets, self._bullet_shape)

            assemble = []
            if grid_players is not None: assemble.append(grid_players)
            if grid_npcs is not None: assemble.append(grid_npcs)
            if grid_bullets is not None: assemble.append(grid_bullets)

            return np.concatenate(assemble, axis=2)



    def _serialize_character(self, k, char):

        def norm_position_relative(v, norm):
            map = norm.game.map
            player = map.players[0]
            return (v - player.attribute.position) / map.bounds.max

        def norm_position_abs(v, norm):
            map = norm.game.map
            return v / map.bounds.max


        attr = char.attribute
        if self._grid_size is None: k.do(attr.position, None, norm_position_abs)
        k.do(attr.hp, None, k.n_div_tag, config.Attr.hp)
