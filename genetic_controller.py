from inspect import getargspec
import random
import copy
import matplotlib.pyplot as plt
import matplotlib.__version__
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import numpy as np


class GeneticController:
    def __init__(self):

# 6.9 Control parameters
# {
    # 19 control parameters
    # 2 major numerical parameters
        self.M          = 500   # Population size
        self.G          = 50    # Maximum number of generations

    # 11 minor numerical parameters
        self.p_c        = .90   # Probability of crossover
        self.p_r        = .10   # Probability of reproduction
        self.p_ip       = .90   # Probability of choosing internal points
        self.D_c        = 17    # Maximum depth for created structures
        self.D_i        = 6     # Maximum depth for initial structures
        self.p_m        = .0    # Probability of mutation
        self.p_p        = .0    # Probability of permutation
        self.f_ed       = 0     # Frequency of editing
        self.p_en       = .0    # Probability of encapsulation
        # NIL           # This var is the condition for decimation, i dont see why it is needed when p_d == .0
        self.p_d        = .0    # Decimation target percentage

    # 6 qualitative variables
        self.generative_method                  = self.ramped_half_and_half   # page 93 # Generative method for the initial random population
        self.first_parent_selection_method      = self.fitness_proportionate    # Method of selection for the first parent in crossover
        self.second_parent_selection_method     = self.fitness_proportionate    # Method of selection for the second parent in crossover
        self.use_adjusted_fitness               = True                          # Optional adjusted fitness measure is used

        if self.M <= 500:                                                       # Over-selection
            self.over_selection                 = False                         # Not used for populations of 500 and below
        if self.M >= 1000:
            self.over_selection                 = True                          # Used for populations of 1000 and above

        self.elitist_strategy                   = False                         # elitist_strategy
# }

    # Other variables
        self.function_type = type(getargspec)
        self.generation = 0
        self.current_generation = []
        self.next_generation = []
        self.r_max = None
        self.worst_fitness = [None] * self.G
        self.average_fitness = [None] * self.G
        self.best_fitness = [None] * self.G
        self.total_adjusted_fitness = [0] * self.G

    # Statistics
        self.n_best_of_population = 10
        self.best_of_population = []
        self.n_best_of_generation = 2
        self.best_of_generation = []
        # histogram

    # 3d graph
        X = np.arange(0, self.G, 1) # gen
        Y = np.arange(0, 201, 10) # fitness
        self.X, self.Y = np.meshgrid(X, Y)
        self.Z = [0]*self.G
        #for i in range(self.G):
        #    self.Z[i] = 20 # asdfsafdsafsafd


    def wrapper(self, arg):
        """return arg unless overrided by subclass"""
        return arg

    def is_function(self, possible_function):
        # Considered a terminal if arity == 0
        if type(possible_function) == self.function_type and len(getargspec(possible_function)[0]) > 0:
            return True
        return False

# 6.2 The Initial Structures
# {

    def full(self, genome, depth):
        """A method to build initial structures where all terminals are the same distance from the top"""
        node = GenomeNode(genome)
        if depth > 1:
            node.set_function(random.choice(self.F))
        else:
            node.set_terminal(random.choice(self.T))

        for i in range(node.arity):
            node.add_child(self.full(genome, depth-1))

        return node
        
    def grow(self, genome, depth, first_node=True):
        """A method to build variably shaped initial structures"""
        node = GenomeNode(genome)

        # first node must be a funciton
        if first_node:
            node.set_function(random.choice(self.F))

        elif depth > 1:
            possible_function = random.choice(self.F + self.T)
            if self.is_function(possible_function):
                node.set_function(possible_function)
            else:
                node.set_terminal(possible_function)

        else:
            node.set_terminal(random.choice(self.T))

        for i in range(node.arity):
            node.add_child(self.grow(genome, depth-1, False))

        return node

    def ramped_half_and_half(self, genome):
        depth = random.randint(2,self.D_i)
        if random.randint(0,1):
            return self.full(genome,depth)
        else:
            return self.grow(genome,depth)

    def build_initial_structures(self):
        i = 0
        while i < self.M:
            genome = Genome()
            genome.first_node = self.generative_method(genome)
            if not self.has_duplicate(genome):
                self.next_generation.append(Organism(genome))
                i += 1
        self.current_generation = copy.deepcopy(self.next_generation)
        self.next_generation = []

# }

    def has_duplicate(self, genome):
        return False
        for organism in self.next_generation:
            if organism.genome == genome:
                return True
        return False

    def test_generation(self):
        for i in range(self.M):
            print self.generation, '\t', i
            self.test_organism(self.current_generation[i])
            if i == 0:
                self.worst_fitness[self.generation] = self.s(i)
                self.average_fitness[self.generation] = self.s(i)
                self.best_fitness[self.generation] = self.s(i)
            else:
                self.average_fitness[self.generation] = (self.average_fitness[self.generation] * i + self.s(i)) / (i+1)
                if self.s(i) > self.worst_fitness[self.generation]:
                    self.worst_fitness[self.generation] = self.s(i)
                elif self.s(i) < self.best_fitness[self.generation]:
                    self.best_fitness[self.generation] = self.s(i)
            self.total_adjusted_fitness[self.generation] += self.a(i,self.generation) #

        hist, edges = np.histogram([round(self.s(i,self.generation)) for i in range(self.M)], bins = 21, range=(0,200))
        #self.Z[self.generation], edges = np.histogram([round(self.s(i,self.generation)) for i in range(self.M)], bins = 20, range=(0,200))
        self.Z[self.generation] = list(hist)
        print hist
        #for i in range(len(hist)):
        #    self.Z[self.generation][i] = hist[i]

# 6.3 Fitness
# {

    def r(self, i, t=None):
        """Raw Fitness"""
        # t ignored for now because only current_generation is recorded
        return self.current_generation[i].raw_fitness

    def s(self, i, t=None):
        """Standardized Fitness
           Adjustment for raw fitness so a lower fitness is always better."""
        if self.r_max:
            return self.r_max - self.r(i,t)
        return self.r(i,t)

    def a(self, i, t=None):
        """Adjusted Fitness
           A value between 0 and 1. The adjusted fitness is bigger for better individuals.
                         1
           a(i,t) = ------------
                     1 + s(i,t)   
        """
        return 1.0 / (1.0 + self.s(i))

    def n(self, i, t=None):
        """Normalized Fitness
           A value between 0 and 1. Larger for better individuals. Sum of normalized fitness values is 1.
                                a(i,t)
           n(i,t) = ---------------------------------
                     sum of a(k,t) for k from 0 to M
        """
        return self.a(i,t) / self.total_adjusted_fitness[self.generation]

# }

# Selection
# {

    def fitness_proportionate(self):
        #individual = random.choice(self.current_generation)
        #while random.random > self.n(individual):
        #    individual = random.choice(current_generation)
        i = random.randint(0,self.M-1)
        while random.random() > self.n(i):
            i = random.randint(0,self.M-1)
        
        return self.current_generation[i]
        
# }

    def make_child(self):
        # Not sure how Koza whould do this
        parent = self.first_parent_selection_method()
        if random.random() < self.p_c:
            child = self.crossover(parent,self.second_parent_selection_method())
            if not self.has_duplicate(child.genome):
                self.next_generation.append(child)
        if random.random() < self.p_r:
            child = self.reproduce(parent)
            if not self.has_duplicate(child.genome):
                self.next_generation.append( self.reproduce(parent) )
        if random.random() < self.p_m:
            child = self.mutate(parent)
            if not self.has_duplicate(child.genome):
                self.next_generation.append( self.mutate(parent) )
        if random.random() < self.p_p:
            child = self.permutate(parent)
            if not self.has_duplicate(child.genome):
                self.next_generation.append( self.permutate(parent) )
        #if random.random() < self.p_d:
        #    decimate

        #if len(self.next_generation) >= self.M:
        #    while len(self.next_generation) > self.M:
        #        self.next_generation.pop()
        #    self.generati

    def make_next_generation(self):
        while len(self.next_generation) < self.M:
            self.make_child()
        self.current_generation = copy.deepcopy(self.next_generation)
        self.next_generation = []
        self.generation += 1

# 6.4 Primary Operations For Modifying Structures
# {

    # 6.4.1 Reproduction
    def reproduce(self,parent):
        """asexual reproduction"""
        child_genome = copy.deepcopy(parent.genome)
        return Organism(child_genome)

    # 6.4.2 Crossover
    def crossover(self, first_parent, second_parent):
        """sexual reproduction"""
        child_genome = copy.deepcopy(first_parent.genome)

        if random.random() < self.p_ip:
            first_node = child_genome.get_random_function() # what if no function
        else:
            first_node = child_genome.get_random_terminal()

        if random.random() < self.p_ip:
            second_node = copy.deepcopy(second_parent.genome).get_random_function() # () around whole thing or just parent.genome ?
        else:
            second_node = copy.deepcopy(second_parent.genome).get_random_terminal()

        first_node = second_node

        return Organism(child_genome)

# }

# 6.5 Secondary Operations
# {

    # 6.5.1 Mutation
#    def mutation
    # 6.5.2 Permutation
    def permutation(self, parent):
        child_genome = copy.deepcopy(parent.genome)
        random.shuffle( child_genome.get_random_function().children )
        return Organism(child_genome)
        
    # 6.5.3 Editing
#    def edit
    # 6.5.4 Encapsulation
#    def encapsulation
    # 6.5.5 Decimation
#    def decimate

# }

    def test_all_generations(self):
        self.build_initial_structures()
        self.test_generation()
        for i in range(1,self.G):
            self.make_next_generation()
            self.test_generation()

    def display_fitness_curves(self):
        try:
            fig = plt.figure()
            ax = fig.gca(projection='3d')

            self.Z = np.array(self.Z)
            self.Z = self.Z.transpose()
            #self.Z = self.X

            surf = ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1, cmap=cm.jet,
                    linewidth=0, antialiased=False)
            ax.set_zlim3d(-1.01, 1.01)

            ax.w_zaxis.set_major_locator(LinearLocator(10))
            ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

            fig.colorbar(surf, shrink=0.5, aspect=5)

        except Exception:
            print 'need matplotlib version 1 or greater. you have version ' + matplotlib.__version__

        t = range(0,len(self.average_fitness))

        l_worst, = plt.plot(t, self.worst_fitness, 'g-o')
        l_average, = plt.plot(t, self.average_fitness, 'b-D')
        l_best, = plt.plot(t, self.best_fitness, 'r-s')

        plt.legend( (l_worst, l_average, l_best), ('worst', 'average', 'best'), 'upper right', shadow=True)
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Fitness Curves')
        #axis([0,len(self.average_fitness),0,])
        plt.show()


class Genome:
    def __init__(self):
        self.nodes = []
        self.function_nodes = []
        self.terminal_nodes = []
        self.actual_args = {}

    def get_random_node(self):
        return random.choice(self.nodes)

    def get_random_function(self):
        if len(self.function_nodes) > 0:
            return random.choice(self.function_nodes)
        else:
            return self.get_random_terminal()

    def get_random_terminal(self):
        return random.choice(self.terminal_nodes)

    def run(self, *args):
        for i in range(len(Genome.formal_args)):
            self.actual_args[Genome.formal_args[i]] = args[i]
        return self.first_node.run()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
        #if len(self.nodes) != len(other.nodes) or \
        #len(self.terminal_nodes) != len(other.terminal_nodes) or \
        #len(self.function_nodes) != len(other.function_nodes):
        #    return False
        #return self.first_node == other.first_node

    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return self.first_node.__repr__()


class GenomeNode:
    def __init__(self, container):
        self.container = container
        self.children = []

    def set_function(self, function):
        self.function = function
        self.arity = len(getargspec(function)[0])

    def set_terminal(self, terminal):
        self.terminal = terminal
        self.arity = 0

    def is_function(self):
        return self.arity > 0

    def add_child(self, child):
        self.children.append(child)
        if child.is_function():
            self.container.function_nodes.append(child)
        else:
            self.container.terminal_nodes.append(child)
        self.container.nodes.append(child)

    def interpret_terminal(self):
        #if type(self.terminal) == str:
        #    return locals()[self.terminal]
        #elif type(self.terminal) == int:
        #    return self.terminal
        #else:
        #    return self.terminal()
        if type(self.terminal) == str:
            return self.container.actual_args.get(self.terminal)
        elif type(self.terminal) == int:
            return self.terminal
        
    def run(self):
        if self.is_function():
            args = []
            for child in self.children:
                args.append(child.run())
            return self.function(*args)
        else:
            return self.interpret_terminal()

    def __eq__(self, other):
        if self.is_function() and other.is_function():
            if len(self.children) != len(other.children) or self.function != other.function:
                return False
            return True
        elif not self.is_function() and not other.is_function():
            if self.terminal == other.terminal:
                return True
            return False
        else:
            return False

    def __repr__(self):
        if self.is_function():
            s = '(' + self.function.__name__ + ' '
            s += ', '.join(repr(c) for c in self.children)
            return s + ')'
        else:
            return '(' + str(self.terminal) + ')'

class Organism:
    def __init__(self, genome):
        self.genome = genome
        #import pdb; pdb.set_trace()
        #self.wrapper = locals()['wrapper']
        self.raw_fitness = None
        #self.hits = None
        self.hits = 0
    def run(self, *args):
        #return self.wrapper(self.genome.run())
        return self.genome.run(*args)
    def __repr__(self):
        return \
        "Raw Fitness: " + str(self.raw_fitness) + "\n" + \
        "Hits: " + str(self.hits) + "\n" + \
        "Function: " + str(self.genome)

