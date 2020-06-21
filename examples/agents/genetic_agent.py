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

    name_of_run = ""

    test_data = []

    mutation_divisor = 100

    maximum_score = 0

    maximum_fitness = 0

    finished_maximum = 0

    finish_portion_after = 0

    best_genome = []

    # the actions that the algorithm picked to be the best.
    # Contains all actions to be performed, not just the ones from this portion of the learning
    actions_to_take = []

    # how many portions of the game have already been learnt, meaning we start at action portion * amount_of_actions
    portion = 0

    env = None

    population = None

    def __init__(self, amount_of_actions, name_of_run, test_data, mutation_divisor, mutations_before_point_of_death, finish_portion_after):

        self.amount_of_actions = amount_of_actions

        self.name_of_run = name_of_run

        self.test_data = test_data

        self.population = test_data

        self.mutation_divisor = mutation_divisor

        self.mutations_before_point_of_death = mutations_before_point_of_death

        self.finish_portion_after = finish_portion_after

        for genome in self.population:

            # from 0 to amount_of_actions - 1
            genome = genome[:amount_of_actions]



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



        self.population = pickle.load(open(name_of_run + '_savepopulation.pkl', 'rb'))

        population_count_file = open("population_count.txt", "r+")

        population_count = int(population_count_file.read())

        genetic_data_file = open(name_of_run + '_genome_performance.txt', "a")

        for k in range(60):

            rewards, fitness, steps = self.calculate_fitness()

            parents = self.select_crossovers(fitness, rewards, steps)

            for i in range(self.amount_of_parents):

                genetic_data_file.write(str(population_count))

                genetic_data_file.write(";")

                genetic_data_file.write(str(parents[i]['fitness']))

                genetic_data_file.write(";")

                genetic_data_file.write(str(parents[i]['reward']))

                genetic_data_file.write(";")

                genetic_data_file.write(str(parents[i]['steps']))

                genetic_data_file.write(";")

                if parents[i]['steps'] == amount_of_actions:
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

            self.mutation()

            pickle.dump(self.population, open(name_of_run + '_savepopulation.pkl', 'wb'))

            self.env.close()



    def threshold(self):

        self.portion = self.portion + 1


    def save_env_state(self):

        self.actions_to_take = numpy.concatenate(self.actions_to_take, self.best_genome)



    def mutation(self, point_of_death):

        for i in range(self.plays_per_population):

            mutation_chance = numpy.random.randint(low=0, high=99)

            amount_of_mutations = self.amount_of_actions / self.mutation_divisor

            if mutation_chance >= 90:

                amount_of_mutations = amount_of_mutations * 5

            else:

                if mutation_chance >= 60:

                    amount_of_mutations = amount_of_mutations * 3

            # only if the plane really crashed
            if point_of_death != self.amount_of_actions:

                # mutations before point_of_death
                for h in range(self.mutations_before_point_of_death):

                    action_to_replace = numpy.random.randint(low=point_of_death - self.mutations_before_point_of_death * 3, high=point_of_death)

                    new_action = numpy.random.randint(low=0, high=17)

                    self.population[h][action_to_replace] = new_action

            # random mutations
            for j in range(amount_of_mutations):

                action_to_replace = numpy.random.randint(low=0, high=self.amount_of_actions - 1)

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

        if self.finish_portion_after <= 0:

            self.threshold()

            return

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

                child = self.perform_crossover(parents[i], parents[j])

                children.append(child)

        return children



    def perform_crossover(self, parent1, parent2):

        child = []

        index_parent1 = parent1['index']

        index_parent2 = parent2['index']

        point_of_death = parent1['steps']

        probability = numpy.random.randint(0, 99)

        swap_start = point_of_death - 10

        if probability > 60:
            swap_start = point_of_death - 50

        if probability > 90:
            swap_start = point_of_death - 100

        if swap_start < 0:
            swap_start = 0

        swap_end = swap_start + 10

        if swap_end > 999:
            swap_end = 999

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

        at_least_one_finished = False

        for h in range(self.plays_per_population):

            reward, step = self.apply_episode(self.population[h])

            fit = reward + 2 * step

            if step == 1000:

                fit = fit + 1000

                at_least_one_finished = true

                if self.maximum_score < reward:
                    self.maximum_score = reward

                if self.maximum_fitness < fitness:
                    self.maximum_fitness = fitness
                    self.actions_to_take = self.population[h]

            fitness.append(fit)

            steps.append(step)

            rewards.append(reward)

        if at_least_one_finished:

            self.finish_portion_after = self.finish_portion_after - 1

        return rewards, fitness, steps


if __name__ == '__main__':
    agent = GeneticAgent()
