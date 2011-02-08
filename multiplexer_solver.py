from genetic_controller import GeneticController, Genome
import random
import itertools
from hal import hal

"""
Termianl set:   A0 A1 A2 D0 ... D7
Function set:   and or not if
"""

class MultiplexerController(GeneticController):
    def __init__(self):
        GeneticController.__init__(self)
        """
            M = 4000,
            G = 51,
            r_max = 2**11,
            bins = 200,
            D_i = 6
        )"""
        self.M = 100
        self.G = 15
        self.r_max = 2**11
        self.bins = 200
        self.init_3d_graph()
    
        # Terminal set
        self.T = ['a0','a1','a2','d0','d1','d2','d3','d4','d5','d6','d7']

        # Function set
        self.F = [AND,OR,NOT,IF]

        Genome.formal_args = ['a0','a1','a2','d0','d1','d2','d3','d4','d5','d6','d7']

        self.fitness_cases = list(itertools.product('01', repeat=11))

    def test_organism(self, individual):
        for case in self.fitness_cases:
            if individual.run( *map(int,case) ) == target_function(*case):
                individual.raw_fitness += 1


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

def target_function(*args):
    S = int(''.join(args[:3]), 2)
    bits = args[3:]
    return int(bits[S])

if __name__ == '__main__':
    """
    print 'will run without run-time-errors but has bugs'
    mc = MultiplexerController()
    mc.test_all_generations()
    mc.display_fitness_curves()
    """
    hal(MultiplexerController)
