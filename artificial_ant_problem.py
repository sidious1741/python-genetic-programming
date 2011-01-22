from genetic_controller import GeneticController, Genome
import random

"""
Terminal set:   left right move
Function set:   if-food-ahead progn2 progn3
"""

class AntController(GeneticController):
    def __init__(self):
        GeneticController.__init__(self)
    
        # Terminal set
        self.T = [left,right,move]

        # Function set
        self.F = []

        Genome.formal_args = [trail]

# Fitness cases ??

    def test_organism(self, ant):
        operations_per_run = len(ant.genome.nodes)
        operations = 0
        trail = SantaFeTrail()
        while operations < 400:
            ant.run(trail)
            operations += operations_per_run

#class SantaFeTrail:


#def left(self)
#def right(self)
#def move(self)

if __name__ == '__main__':
    print 'Not yet implemented'
    #ac = AntController()
    #ac.test_all_generations()
    #ac.display_fitness_curves()

