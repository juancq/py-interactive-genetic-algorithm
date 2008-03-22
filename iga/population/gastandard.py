
class Gastandard:
    def __init__(self, paramClass, paramDict):
        self.params = paramClass
        self.popsize = paramDict['size']
        self.paramDict = paramDict

        select = paramDict['selection']
        execstr = 'from %s import %s as selectfunc' % (select, select)
        exec(execstr)
        self.selectfunc = selectfunc

        combinepop = paramDict['combinepop']
        execstr = 'from %s import %s as combinepopfunc' % (combinepop, combinepop)
        exec(execstr)
        self.combinepopfunc = combinepopfunc

        self.pop = self.params.app.createPop(self.popsize)
        self.totalFitness = 0.0
        self.childpop = []


#---------------------------------------#
    def eval(self, pop=None):
        if not pop:
            pop = self.pop

        fitness_func = self.params.app.fitness
        for ind in pop:
            fitness_func(ind)
        # scale fitness of population
        self.params.app.scaleFitness(pop)


#---------------------------------------#
    def selectParent(self):
        return self.selectfunc(self.pop, self.params.random)

#---------------------------------------#
    def combinepop(self, newPop):
        self.pop = self.combinepopfunc(self.pop, newPop)

#---------------------------------------#
    def crossover(self, parent1, parent2):
        child1, child2 = self.params.crossover(parent1, parent2)
        return child1, child2

#---------------------------------------#
    def nextgen(self):
        '''
        Create next generation from current population.
        '''
        newPop = []
        for i in xrange(0, self.popsize, 2):
            p1 = self.selectParent()
            p2 = self.selectParent()
            c1, c2 = self.crossover(p1, p2)
            self.params.mutate(c1)
            self.params.mutate(c2)
            newPop.extend([c1, c2])

        self.eval(newPop)
        self.combinepop(newPop)

#---------------------------------------#
