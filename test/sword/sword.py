

import time
import gym
import config as game_config

#config.NUM_NPC = 1

#config.BASE_PLAYER.max_hp = 10**3

def run(render=False):
    env = gym.make(game_config.GAME_NAME)
    env = env.unwrapped
    env.reset()

    while True:
        if env.terminal: env.reset()
        time.sleep(1.0/600)
        env.step([0, env.game.map.npcs[0]])
        if render: env.render()


if __name__  == '__main__':
    run(True)
