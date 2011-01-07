from genetic_controller import GeneticController, Genome
import random

class CartController(GeneticController):
    def __init__(self):
        GeneticController.__init__(self)
    
        # Terminal set
        self.T = ['x','v',-1]

        # Function set
        self.F = [add,sub,mul,div,gt,ABS]

        Genome.formal_args = ['x','v']

# Fitness cases ??

    def test_organism(self, centerer):
        """This method should test a given organism and assign asfasdfsaf"""
        total_time = 0
        for i in range(20):
            v = 1.5 * random.random() - .75
            x = 1.5 * random.random() - .75
            t = 0
            while t < 10 and (abs(v) > .01 or abs(x) > .01):
                thrust = centerer.run(x,v)
                v += thrust * .02
                x += v * .02
                t += .02
            if t < 10:
                centerer.hits += 1
            total_time += t
        centerer.raw_fitness = total_time


def add(a,b): return a+b
add.__name__ = '+'
def sub(a,b): return a-b
sub.__name__ = '-'
def mul(a,b): return a*b
mul.__name__ = '*'
def div(a,b):
    if b == 0:
        return 1
    else:
        return a/b
div.__name__ = '%'
def gt(a,b): 
    return int(a<b)*2-1
def ABS(a): ###################################
    return abs(a)
"""def X:
    return locals('self.x')
def V:
    return locals('self.v')
"""


cc = CartController()
cc.test_all_generations()
cc.display_fitness_curves()

"""
classes GeneticFunctions and GeneticTerminals
a Resources class
organism does not need variables, test_organism and genome do
dont extend organism
put all of genetic_controller in genome
"""
