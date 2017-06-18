
import gym
from gymgame.tinyrpg.ball import config
import time


env = gym.make(config.GAME_NAME)
env.reset()

while True:
    time.sleep(1.0)
    env.step([])