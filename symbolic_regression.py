from genetic_controller import GeneticController, Genome
import random, math

"""
Terminal set:   X
Function set:   + - * % sin cos exp rlog
"""

class RegressionController(GeneticController):
    def __init__(self):
        GeneticController.__init__(self)
        self.M = 500
        self.G = 51
        self.r_max = 20
        self.bins = 20
        self.init_3d_graph()

        # Terminal set
        self.T = ['x']

        # Function set
        self.F = [add,sub,mul,div,sin,cos,exp,rlog]

        Genome.formal_args = ['x']

# Fitness cases ??

    def test_organism(self, individual):
        for i in range(20):
            x = random.random()*2 - 1  # [-1,+1]
            fitness_case = (x,target_function(x))
            error = abs( individual.run( fitness_case[0] ) - fitness_case[1] )
            if error < .01:
                individual.hits += 1
            individual.raw_fitness += error

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
def sin(a):
    return math.sin(a)
def cos(a):
    return math.cos(a)
def exp(a):
    return math.exp(a)
def rlog(a):
    if a > 0:
        return math.log(a)
    else:
        return 0

def target_function(x):
    return x**4 + x**3 + x**2 + x

if __name__ == '__main__':
    #print 'Not yet implemented'
    rc = RegressionController()
    rc.test_all_generations()
    rc.display_fitness_curves()

