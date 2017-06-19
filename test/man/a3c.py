import tensorflow as tf
import numpy as np



class ACNet(object):
    def __init__(self,
                 sess, scope, n_state, n_action, optimizer,
                 global_ac=None,
                 entropy_beta=0.001):
        self.sess = sess
        self.scope = scope
        self.n_state = n_state
        self.n_action = n_action
        self.optimizer = optimizer
        self.global_ac = global_ac


        if global_ac is None:  # get global network
            with tf.variable_scope(scope):
                self.s = tf.placeholder(tf.float32, [None, n_state], 'S')
                self._build_net()
                self.a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
                self.c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')
        else:  # local net, calculate losses
            with tf.variable_scope(scope):
                self.s = tf.placeholder(tf.float32, [None, n_state], 'S')
                self.a_his = tf.placeholder(tf.int32, [None, ], 'A')
                self.v_target = tf.placeholder(tf.float32, [None, 1], 'Vtarget')

                self.a_prob, self.v = self._build_net()

                td = tf.subtract(self.v_target, self.v, name='TD_error')
                with tf.name_scope('c_loss'):
                    self.c_loss = tf.reduce_mean(tf.square(td))

                with tf.name_scope('a_loss'):
                    log_prob = tf.reduce_sum(tf.log(self.a_prob) * tf.one_hot(self.a_his, n_action, dtype=tf.float32),
                                             axis=1, keep_dims=True)
                    exp_v = log_prob * td
                    entropy = -tf.reduce_sum(self.a_prob * tf.log(self.a_prob), axis=1,
                                             keep_dims=True)  # encourage exploration
                    self.exp_v = entropy_beta * entropy + exp_v
                    self.a_loss = tf.reduce_mean(-self.exp_v)

                with tf.name_scope('local_grad'):
                    self.a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
                    self.c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')
                    self.a_grads = tf.gradients(self.a_loss, self.a_params)
                    self.c_grads = tf.gradients(self.c_loss, self.c_params)

            with tf.name_scope('sync'):
                with tf.name_scope('pull'):
                    self.pull_a_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.a_params, global_ac.a_params)]
                    self.pull_c_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.c_params, global_ac.c_params)]
                with tf.name_scope('push'):
                    self.update_a_op = optimizer.apply_gradients(zip(self.a_grads, global_ac.a_params))
                    self.update_c_op = optimizer.apply_gradients(zip(self.c_grads, global_ac.c_params))

    def _build_net(self):
        w_init = tf.random_normal_initializer(0., .1)
        with tf.variable_scope('actor'):
            l_a = tf.layers.dense(self.s, 200, tf.nn.relu6, kernel_initializer=w_init, name='la')
            a_prob = tf.layers.dense(l_a, self.n_action, tf.nn.softmax, kernel_initializer=w_init, name='ap')
        with tf.variable_scope('critic'):
            l_c = tf.layers.dense(self.s, 100, tf.nn.relu6, kernel_initializer=w_init, name='lc')
            v = tf.layers.dense(l_c, 1, kernel_initializer=w_init, name='v')  # state value
        return a_prob, v

    def update_global(self, feed_dict):  # run by a local
        self.sess.run([self.update_a_op, self.update_c_op], feed_dict)  # local grads applies to global net

    def pull_global(self):  # run by a local
        self.sess.run([self.pull_a_params_op, self.pull_c_params_op])

    def choose_action(self, s):  # run by a local
        prob_weights = self.sess.run(self.a_prob, feed_dict={self.s: s[np.newaxis, :]})
        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights.ravel())  # select action w.r.t the actions prob
        return action


class Worker(object):
    def __init__(self, ac, env, gamma=0.9):
        self.env = env
        self.gamma = gamma
        self.AC = ac

    def work(self, sess, update_nsteps=20, should_stop=None, step_callback=None, train_callback=None):
        total_step = 1
        buffer_s, buffer_a, buffer_r = [], [], []
        while (should_stop is None) or (not should_stop()):
            s = self.env.reset()

            # if GLOBAL_EP % 1 == 0:
            #     saver.save(SESS, "models-pig/a3c-sw1-player", global_step=GLOBAL_EP)
            while True:
                a = self.AC.choose_action(s)
                s_, r, done, info = self.env.step(a)
                print('action:', a, 'reward:', r)
                buffer_s.append(s)
                buffer_a.append(a)
                buffer_r.append(r)

                if total_step % update_nsteps == 0 or done:  # update global and assign to local net
                    if done:
                        v_s_ = 0  # terminal
                    else:
                        v_s_ = sess.run(self.AC.v, {self.AC.s: s_[np.newaxis, :]})[0, 0]
                    buffer_v_target = []
                    for r in buffer_r[::-1]:  # reverse buffer r
                        v_s_ = r + self.gamma * v_s_
                        buffer_v_target.append(v_s_)
                    buffer_v_target.reverse()

                    buffer_s, buffer_a, buffer_v_target = np.vstack(buffer_s), np.array(buffer_a), np.vstack(
                        buffer_v_target)
                    feed_dict = {
                        self.AC.s: buffer_s,
                        self.AC.a_his: buffer_a,
                        self.AC.v_target: buffer_v_target,
                    }
                    self.AC.update_global(feed_dict)

                    buffer_s, buffer_a, buffer_r = [], [], []
                    self.AC.pull_global()

                    if train_callback is not None: train_callback()

                s = s_
                total_step += 1
                if step_callback is not None: step_callback()

                if done: break



