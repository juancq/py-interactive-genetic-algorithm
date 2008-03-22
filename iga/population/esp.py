from standard import Standard
import sys

class Esp(Standard):
    def __init__(self, paramClass, paramDict):
        Standard.__init__(self, paramClass, paramDict)
        self.permutations = paramDict['permutations']

    def eval(self, pop=None):
        if not pop:
            pop = self.pop

        evalsets = []
        for i in xrange(len(pop)):
            subpop = pop[i]
            permset = []
            for j in xrange(self.permutations):
                self.params.random.shuffle(subpop)
                permset.extend(subpop)
            evalsets.append(permset)

        print "%.2f" % 0.0,
        sys.stdout.flush()
        numevals = self.popsize*self.permutations
        for i in xrange(numevals):
            evalset = []
            for subset in evalsets:
                evalset.append(subset[i])
            self.params.app.fitness(evalset)
            print "\r", " " * 60,
            print "\r%.2f" % ((i+1)/float(numevals)*100),
            sys.stdout.flush()
        print "\r", " " * 60,

    def selectParent(self, pop):
        return self.selectfunc(pop, self.params.random)

    def combinepop(self, newPop):
        for i in xrange(len(self.pop)):
            self.pop[i] = self.combinepopfunc(self.pop[i], newPop[i])

    def nextgen(self):
        newpop = []
        for subpop in self.pop:
            newsubpop = []
            for i in xrange(0, self.popsize, 2):
                p1 = self.selectParent(subpop)
                p2 = self.selectParent(subpop)
                c1, c2 = self.params.crossover(p1, p2)
                self.params.mutate(c1)
                self.params.mutate(c2)
                newsubpop.append(c1)
                newsubpop.append(c2)
            newpop.append(newsubpop)
        self.eval(newpop)
        self.params.app.scaleFitness(newpop)
        self.combinepop(newpop)
