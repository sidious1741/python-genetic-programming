from genetic_controller import GeneticController, Genome
import random

class RegressionController(GeneticController):
    def __init__(self):
        GeneticController.__init__(self)
    
        # Terminal set
        self.T = []

        # Function set
        self.F = []

        Genome.formal_args = []

# Fitness cases ??

    def test_organism(self):
        return

if __name__ == '__main__':
    print 'Not yet implemented'
    #rc = RegressionController()
    #rc.test_all_generations()
    #rc.display_fitness_curves()

