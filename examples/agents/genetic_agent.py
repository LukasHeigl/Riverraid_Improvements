import argparse
# import sys
import numpy

import pickle

import gym
from gym import wrappers, logger


class GeneticAgent(object):
    """A genetic algorithm approach to River raid"""

    plays_per_population = 100

    amount_of_parents = 10

    amount_of_actions = 1000

    population_count = 0

    env = None

    population = None

    def __init__(self):

        parser = argparse.ArgumentParser(description=None)
        parser.add_argument('env_id', nargs='?', default='Riverraid-ram-v0', help='Select the environment to run')
        args = parser.parse_args()

        # You can set the level to logger.DEBUG or logger.WARN if you
        # want to change the amount of output.
        logger.set_level(logger.INFO)

        self.env = gym.make(args.env_id)

        self.env = wrappers.AtariPreprocessing(self.env)

        self.env.seed(0)

        #self.population = self.createpopulation()



        self.population = pickle.load(open('savepopulation.pkl', 'rb'))

        population_count_file = open("population_count.txt", "r+")

        population_count = int(population_count_file.read())

        genetic_log_file = open("geneticLog.txt", "a")

        genetic_data_file = open("geneticData.txt", "a")

        for k in range(20):

            genetic_log_file.write("Population number ")

            genetic_log_file.write(str(population_count))

            genetic_log_file.write(":\n")





            rewards, fitness, steps = self.calculate_fitness()

            parents = self.select_crossovers(fitness, rewards, steps)

            genetic_log_file.write("Parents scores:\n")


            for i in range(self.amount_of_parents):

                genetic_log_file.write(str(parents[i]['fitness']))

                genetic_log_file.write("\n")

                genetic_data_file.write(str(population_count))

                genetic_data_file.write(";")

                genetic_data_file.write(str(parents[i]['fitness']))

                genetic_data_file.write(";")

                genetic_data_file.write(str(parents[i]['reward']))

                genetic_data_file.write(";")

                genetic_data_file.write(str(parents[i]['steps']))

                genetic_data_file.write(";")

                if parents[i]['steps'] == 1000:
                    genetic_data_file.write("1")
                else:
                    genetic_data_file.write("0")

                genetic_data_file.write(";")

                genetic_data_file.write("\n")

            children = self.create_children(parents)

            population_count = population_count + 1

            #putting the position at the beginning, to delete the line with truncate
            population_count_file.seek(0)

            population_count_file.truncate()

            population_count_file.write(str(population_count))

            self.population = children

            pickle.dump(self.population, open('savepopulation.pkl', 'wb'))

            self.mutation()

            self.env.close()



    '''
        runs the environment with the actions specified in chromosome
        returns the reward and the amount of actions taken before either done was returned (death),
        or all given actions were performed
    '''

    def mutation(self):

        for i in range(self.plays_per_population):

            mutation_chance = numpy.random.randint(low=0, high=99)

            amount_of_mutations = 10

            if mutation_chance > 90:

                amount_of_mutations = 50

            else:

                if mutation_chance > 60:

                    amount_of_mutations = 25

            for j in range(amount_of_mutations):

                action_to_replace = numpy.random.randint(low=0, high=999)

                new_action = numpy.random.randint(low=0, high=17)

                self.population[i][action_to_replace] = new_action






    def apply_episode(self, chromosome):

        episode_reward = 0
        steps_performed = 0

        self.env.reset()

        for i in range(len(chromosome)):

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


    def create_children(self, parents):

        children = []

        for i in range(self.amount_of_parents):

            for j in range(self.amount_of_parents):

                child = self.perform_crossover(parents[i]['index'], parents[j]['index'])

                children.append(child)

        return children

    def perform_crossover(self, index_parent1, index_parent2):

        child = []

        swap_start = numpy.random.randint(0, (self.amount_of_actions / 2) - 1)

        swap_end = numpy.random.randint(self.amount_of_actions / 2, self.amount_of_actions)

        child = self.population[index_parent1][:swap_start]

        child = numpy.append(child, self.population[index_parent2][swap_start:swap_end])

        if swap_end < self.amount_of_actions:

            child = numpy.append(child, self.population[index_parent2][swap_end:self.amount_of_actions])

        return child



    def select_crossovers(self, fitness, rewards, steps):

        indexed_fitness = []

        for j in range(self.plays_per_population):

            entry = {

                "index": j,
                "fitness": fitness[j],
                "reward": rewards[j],
                "steps": steps[j]
            }


            indexed_fitness.append(entry)

        newlist = sorted(indexed_fitness, key=lambda k: k['fitness'], reverse=True)

        parents = []

        for k in range(self.amount_of_parents):

            parents.append(newlist[k])

        return parents



    def calculate_fitness(self):

        rewards = []

        steps = []

        fitness = []

        for h in range(self.plays_per_population):

            reward, step = self.apply_episode(self.population[h])

            fit = reward + step

            if step == 1000:
                fit = fit + 1000

            fitness.append(fit)

            steps.append(step)

            rewards.append(reward)

        return rewards, fitness, steps


if __name__ == '__main__':
    agent = GeneticAgent()
