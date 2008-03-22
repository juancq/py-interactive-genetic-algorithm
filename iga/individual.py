counter = 0
import copy

class Individual:
    def __init__(self, random, length, genome=None):
        global counter
        self.fitness = 0.0
        self.scalefit = 0.0
        self.id = counter
        self.bloodline = 0.
        counter += 1
        self.from_p1 = 0.5
        self.from_p2 = 0.5

        if not genome:
            self.genome = [random.randint(0,1) for i in xrange(0, int(length))]
        else:
            self.genome = copy.deepcopy(genome)

    def isequal(self, other):
        return self.__cmp__(other)

    def __cmp__(self, other):
        return cmp(self.fitness, other.fitness)
