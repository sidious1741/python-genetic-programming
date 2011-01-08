from genetic_controller import GeneticController, Genome
import random

class MultiplexerController(GeneticController):
    def __init__(self):
        GeneticController.__init__(self)
    
        # Terminal set
        self.T = ['a0','a1','a2','d0','d1','d2','d3','d4','d5','d6','d7']

        # Function set
        self.F = [AND,OR,NOT,IF]

        Genome.formal_args = ['a0','a1','a2','d0','d1','d2','d3','d4','d5','d6','d7']

        self.fitness_cases = range(0,2**11)

    def test_organism(self, individual):
        for case in self.fitness_cases:
            self.test_fitness_case(individual, case)

    def test_fitness_case(self, individual, case):
        pass

def AND(a,b):
    return a and b
def OR(a,b):
    return a or b
def NOT(a):
    return not a
def IF(a,b,c):
    if a:
        return b
    else:
        return c

if __name__ == '__main__':
    print 'Not yet implemented'
    #mc = MultiplexerController()
    #mc.test_all_generations()
    #mc.display_fitness_curves()

