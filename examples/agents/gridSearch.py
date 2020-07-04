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
    # this is reset every time a better solution is found
    finish_portion_after_sample = {10, 50, 100, 250, 500}

    # how many portions were learned for what learning session
    progress = {"test": 0}

    # saves the learned (best) actions
    actions_to_take = {"test": []}

    # saves the maximum score
    actual_score = {"test": 0}

    required_populations = {"test": 0}

    test_data = []

    test_data_size = 5000

    init_learning()


def init_learning(self):

    self.test_data = numpy.random.randint(low=0, high=18, size=self.test_data_size)

    # if there was enough time, every possible combination of the parameters should be tested multiple times

    start_learning_session(self.amount_of_actions_sample[0], "firstRun100", self.mutation_divisor_sample[0],
                           self.mutations_before_point_of_death_sample[2], self.finish_portion_after_sample[2]
                           , 50)

    continue_learning_session("firstRun100", 50)


# test_data must contain the test_data for the whole planned learning
# it must be divided into portions containing exactly amount_of_actions actions
def start_learning_session(self, amount_of_actions, name_of_run, mutation_divisor, mutations_before_point_of_death,
                           finish_portion_after, population_runs):

    geneticAgent = GeneticAgent(amount_of_actions, name_of_run, self.test_data[self.progress[name_of_run]],
                                mutation_divisor, mutations_before_point_of_death, finish_portion_after)

    pickle.dump(geneticAgent, open(name_of_run + '_agent.pkl', 'wb'))




def continue_learning_session(self, name_of_run, population_runs):

    geneticAgent = pickle.load(open(name_of_run + '_agent.pkl', 'rb'))

    is_finished, best_genome, required_populations, maximum_score = \
        geneticAgent.run_portion(self.test_data[self.progress[name_of_run]], population_runs)

    pickle.dump(geneticAgent, open(name_of_run + '_agent.pkl', 'wb'))

    if is_finished:

        self.progress[name_of_run] = self.progress[name_of_run] + 1

        numpy.append(self.actions_to_take[name_of_run], best_genome)

        self.actual_score[name_of_run] = maximum_score

        self.required_populations[name_of_run] = required_populations














