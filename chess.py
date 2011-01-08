from genetic_controller import GeneticController, Genome
import random

class ChessController(GeneticController):
    def __init__(self):
        GeneticController.__init__(self)
    
        # Terminal set
        self.T = []

        # Function set
        self.F = []

        Genome.formal_args = []

# Fitness cases ??

    def test_organism(self, player_one):
        """fitness will be based on time it takes to move, makes a move, kills a guy, and traps the king"""
        if self.player_one.raw_fitness == None:
            return
        player_two = random.choice(self.current_generation)


#class ChessBoard:
#    def __init__(self, 


if __name__ == '__main__':
    print 'Not yet implemented'
    #cc = ChessController()
    #cc.test_all_generations()
    #cc.display_fitness_curves()
