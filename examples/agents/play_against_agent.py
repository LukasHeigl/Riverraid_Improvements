from examples.agents.genetic_agent import GeneticAgent
from examples.agents.keyboard_agent import KeyboardAgent

import numpy
import threading


class PlayAgainstAgent(object):
    """With this class, a player can play against a given agent side by side"""

    agent1 = None

    agent2 = None

    window1 = None




    def __init__(self, Agent1, Agent2):

        self.agent1 = Agent1

        self.agent2 = Agent2

        t1 = threading.Thread(target=self.agent1.start)

        #t2 = threading.Thread(target=self.agent2.start)

        t1.start()

        while self.agent1.window == None:
            print("Warten...")

        self.window1 = self.agent1.window

        self.window1.height = 400

        print("Schluss")




if __name__ == '__main__':
    keyboardAgent = KeyboardAgent()
    playAgainstAgent = PlayAgainstAgent(keyboardAgent, None)
