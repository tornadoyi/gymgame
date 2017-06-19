


import gym
from gymgame.tinyrpg.man import config
import time


def run(render=False):
    env = gym.make(config.GAME_NAME)
    env.reset()

    while True:
        if env.env.terminal: env.reset()
        time.sleep(1.0/60)
        env.step([])
        if render: env.render()


if __name__  == '__main__':
    run()
