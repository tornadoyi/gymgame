"""
Human interact with gym env
pip install pynput
"""
import numpy as np
import time
import gym
import config
from pynput import keyboard
from pynput.keyboard import Key
import pickle
import copy
from gymgame.engine import Vector2
import time

record_dir = './replay.pkl'

class Round(object):
    def __init__(self):
        self.states = []
        self.actions = []


    def save(self, env, a):

        def _data(o):
            attr = o.attribute
            pos, dir = attr.position, attr.direct
            return np.hstack([pos, dir])

        game = env.game
        map = game.map
        player = map.players[0]
        bullets = map.bullets

        list = [_data(player)] + [_data(bullet) for bullet in bullets]
        s = np.hstack(list)


        self.states.append(s)
        self.actions.append(a)




def listen_to_mouse():
    from pynput import mouse

    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0}'.format(
            (x, y)))

    # Collect events until released
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()


def listen_to_keyboard():
    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def record(render=False):
    env = gym.make(config.GAME_NAME)
    env.reset()

    ACTION_KEYS = [Key.up, Key.right, Key.down, Key.left]

    rounds = []
    rnd = Round()

    demos = []

    def on_press(key):
        if key not in ACTION_KEYS: return

        nonlocal rnd
        a = ACTION_KEYS.index(key)
        rnd.save(env, a)

        s = env.state
        s_, r, d, _ = env.step(ACTION_KEYS.index(key))

        demo = dict(state=s, action=a, reward=r, terminal=d,
                    internal=[])
        demos.append(demo)

        if render: env.render()
        if env.terminal:
            rnd.save(env, 0)
            env.reset()
            rounds.append(rnd)
            rnd = Round()

            # save to file
            print('save to file')
            with open(record_dir, 'wb') as f:
                pickle.dump(demos, f, pickle.HIGHEST_PROTOCOL)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()





def replay(render=False):
    with open(record_dir, 'rb') as f:
        rounds = pickle.load(f)

    env = gym.make(config.GAME_NAME)

    for rnd in rounds:
        env.reset()
        map = env.game.map

        for i in range(len(rnd.states)):
            s = rnd.states[i]

            player = map.players[0]
            player.attribute.position = Vector2(*s[0:2])
            player.direct = Vector2(*s[2:4])

            bullets = map.bullets
            for i in range(len(bullets)):
                bullet = bullets[i]
                idx = (i + 1) * 4
                s_bullet = s[idx:idx+4]
                bullet.attribute.position = Vector2(*s_bullet[0:2])
                bullet.direct = Vector2(*s_bullet[2:4])

            if render:
                env.render()
                time.sleep(0.1)

    print('end')







if __name__ == '__main__':
    # listen_to_keyboard()
    # listen_to_mouse()
    replay()
