import argparse
import sys
import numpy

import gym
from gym import wrappers, logger

class GeneticAgent(object):
    """A genetic algorithm approach to River raid"""

    plays_per_population = 10

    amount_of_actions = 1000

    env = None

    population = None

    def __init__(self, action_space):
        self.action_space = action_space

        parser = argparse.ArgumentParser(description=None)
        parser.add_argument('env_id', nargs='?', default='Riverraid-ram-v0', help='Select the environment to run')
        args = parser.parse_args()

        # You can set the level to logger.DEBUG or logger.WARN if you
        # want to change the amount of output.
        logger.set_level(logger.INFO)

        self.env = gym.make(args.env_id)

        self.env.seed(0)

        population = self.createpopulation()

        rewards = self.calculate_fitness()






    '''
        runs the environment with the actions specified in chromosome
        returns the reward and the amount of actions taken before either done was returned (death),
        or all given actions were performed
    '''
    def apply_episode(self, chromosome):

        episode_reward = 0
        steps_performed = 0

        self.env.reset()

        for i in range(chromosome):

            _, reward, done, _ = self.env.step(chromosome[i])

            steps_performed = steps_performed + 1

            episode_reward = episode_reward + reward

            if done:

                break

        return episode_reward, steps_performed



    def act(self, observation, reward, done):
        return self.action_space.sample()


    def createpopulation(self):

        population_size = (self.plays_per_population, self.amount_of_actions)

        new_population = numpy.random.randint(low=0, high=18, size=population_size)
        return new_population



    def calculate_fitness(self):

        rewards = None

        for h in range(self.population):

            rewards[h] = self.apply_episode(self.population[h])

        return rewards



if __name__ == '__main__':

    episode_count = 2000
    reward = 0
    done = False

    outF = open("rewardLog.txt", "w")

    for i in range(episode_count):
        ob = env.reset()
        t = 0
        r = 0
        while True:
            action = agent.act(ob, reward, done)
            #print("Action: ", str(action))

            ob, reward, done, _ = env.step(action)
            t = t + 1
            r = r + reward
            #outF.write(env.observation_space)
            if done:
                print(i, t, r)
                outF.write(str(i))
                outF.write(", ")
                outF.write(str(t))
                outF.write(", ")
                outF.write(str(r))
                outF.write("\n")
                break
            # Note there's no env.render() here. But the environment still can open window and
            # render if asked by env.monitor: it calls env.render('rgb_array') to record video.
            # Video is not recorded every episode, see capped_cubic_video_schedule for details.

    outF.close()
    # Close the env and write monitor result info to disk
    env.close()
