


import gym
from gymgame.tinyrpg.man import config
import time


def run(with_render=False):
    env = gym.make(config.GAME_NAME)
    env.reset()

    while True:
        time.sleep(1.0/60)
        env.step([])
        if with_render: env.render()


run()