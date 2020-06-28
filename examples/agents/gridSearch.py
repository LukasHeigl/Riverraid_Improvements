from examples.agents.genetic_agent import GeneticAgent

import numpy

import pickle

class GridSearch(object):
    """Grid Search applied to the genetic agent for riverraid"""


def __init__(self):

    all_learned_actions = []

    # how many actions have to be learned per portion
    amount_of_actions_sample = {100, 250, 500, 750, 1000}

    # amount_of_mutations = amount_of_actions / mutation_divisor
    mutation_divisor_sample = {5, 10, 25, 50, 100}

    # only performed if the plane crashed
    mutations_before_point_of_death_sample = {1, 2, 5, 10, 20}

    # if a genome completed the portion successfully,
    # how many populations should be performed until we settle with the best genome
    finish_portion_after_sample = {10, 50, 100, 250, 500}

    # how many portions were learned for what learning session
    progress = {"test": 0}

# test_data must contain the test_data for the whole planned learning
# it must be divided into portions containing exactly amount_of_actions actions
def start_learning_session(self, amount_of_actions, name_of_run, test_data, mutation_divisor, mutations_before_point_of_death, finish_portion_after, population_runs):

    geneticAgent = GeneticAgent(amount_of_actions, name_of_run, test_data[self.progress[name_of_run]], mutation_divisor, mutations_before_point_of_death, finish_portion_after)




def continue_learning_session(self, name_of_run):
    is_finished, best_genome, required_populations, maximum_score = geneticAgent.run_portion(test_data, population_runs)

    pickle.dump(self.population, open(name_of_run + '_agent.pkl', 'wb'))

    if is_finished:
        self.progress[name_of_run] = self.progress[name_of_run] + 1












