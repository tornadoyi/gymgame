import tensorflow as tf
import threading
import gym
import os
import shutil
from a3c import Worker, ACNet
import gym
from gymgame.tinyrpg.man import config
import time


LR_A = 0.001  # learning rate for actor
LR_C = 0.001  # learning rate for critic

OUTPUT_GRAPH = True
LOG_DIR = './log'
N_WORKERS = 1
MAX_GLOBAL_EP = 30000
GLOBAL_NET_SCOPE = 'Global_Net'
UPDATE_GLOBAL_ITER = 20
GAMMA = 0.9
ENTROPY_BETA = 0.001


GLOBAL_EP = 0

env = gym.make(config.GAME_NAME)

N_S = env.observation_space.shape[0]
N_A = env.action_space.n
env.close()


SESS = tf.Session()

with tf.device("/cpu:0"):
    OPT_A = tf.train.RMSPropOptimizer(LR_A, name='RMSPropA')
    #OPT_C = tf.train.RMSPropOptimizer(config.LR_C, name='RMSPropC')
    GLOBAL_AC = ACNet(SESS, GLOBAL_NET_SCOPE, N_S, N_A, OPT_A, entropy_beta=ENTROPY_BETA)  # we only need its params
    workers = []
    # Create worker
    for i in range(N_WORKERS):
        i_name = 'W_%i' % i  # worker name
        env = gym.make(config.GAME_NAME)
        ac = ACNet(SESS, i_name, N_S, N_A, OPT_A, global_ac=GLOBAL_AC, entropy_beta=ENTROPY_BETA)
        workers.append(Worker( ac, env, GAMMA))

COORD = tf.train.Coordinator()
saver = tf.train.Saver()
SESS.run(tf.global_variables_initializer())


if OUTPUT_GRAPH:
    if os.path.exists(LOG_DIR):
        shutil.rmtree(LOG_DIR)
    tf.summary.FileWriter(LOG_DIR, SESS.graph)

worker_threads = []
for worker in workers:
    job = lambda: worker.work(SESS)
    t = threading.Thread(target=job)
    t.start()
    worker_threads.append(t)
COORD.join(worker_threads)