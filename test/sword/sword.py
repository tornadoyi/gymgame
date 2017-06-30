

import time
import gym
from gymgame.tinyrpg.sword import config



def run(render=False):
    env = gym.make(config.GAME_NAME)
    env.reset()

    while True:
        if env.env.terminal: env.reset()
        time.sleep(1.0/600)
        env.step([])
        if render: env.render()


if __name__  == '__main__':
    run(False)
