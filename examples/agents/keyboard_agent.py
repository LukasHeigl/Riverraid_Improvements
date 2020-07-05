#!/usr/bin/env python
import sys, gym, time

#
# Test yourself as a learning agent! Pass environment name as a command-line argument, for example:
#
# python keyboard_agent.py SpaceInvadersNoFrameskip-v4
#

class KeyboardAgent(object):

    env = None

    SKIP_CONTROL = 0  # Use previous control decision SKIP_CONTROL times, that's how you
    # can test what skip is still usable.

    human_agent_action = 0
    human_wants_restart = False
    human_sets_pause = False

    ACTIONS = None

    window = None







    def __init__(self):

        self.env = gym.make('Riverraid-ram-v0' if len(sys.argv) < 2 else sys.argv[1])

        if not hasattr(self.env.action_space, 'n'):
            raise Exception('Keyboard agent only supports discrete action spaces')
        self.ACTIONS = self.env.action_space.n

        print("ACTIONS={}".format(self.ACTIONS))
        print("Press keys 1 2 3 ... to take actions 1 2 3 ...")
        print("No keys pressed is taking action 0")



    def start(self):

        self.env.render()
        self.env.unwrapped.viewer.window.on_key_press = self.key_press
        self.env.unwrapped.viewer.window.on_key_release = self.key_release

        self.window = self.env.unwrapped.viewer.window

        print("ACTIONS={}".format(self.ACTIONS))
        print("Press keys 1 2 3 ... to take actions 1 2 3 ...")
        print("No keys pressed is taking action 0")

        while 1:
            window_still_open = self.rollout(self.env)
            if window_still_open == False: break



    def key_press(self, key, mod):
        if key == 0xff0d: self.human_wants_restart = True
        if key == 32: self.human_sets_pause = not self.human_sets_pause
        a = int(key - ord('0'))
        if a <= 0 or a >= self.ACTIONS: return
        self.human_agent_action = a


    def key_release(self, key, mod):
        a = int(key - ord('0'))
        if a <= 0 or a >= self.ACTIONS: return
        if self.human_agent_action == a:
            self.human_agent_action = 0


    def rollout(self, env):
        self.human_wants_restart = False
        obser = env.reset()
        skip = 0
        total_reward = 0
        total_timesteps = 0
        while 1:
            if not skip:
                # print("taking action {}".format(human_agent_action))
                a = self.human_agent_action
                total_timesteps += 1
                skip = self.SKIP_CONTROL
            else:
                skip -= 1

            obser, r, done, info = env.step(a)
            if r != 0:
                print("reward %0.3f" % r)
            total_reward += r
            window_still_open = env.render()
            if window_still_open == False: return False
            if done: break
            if self.human_wants_restart: break
            while self.human_sets_pause:
                env.render()
                time.sleep(0.1)
            time.sleep(0.1)
        print("timesteps %i reward %0.2f" % (total_timesteps, total_reward))


if __name__ == '__main__':
        keyboard_agent = KeyboardAgent()



