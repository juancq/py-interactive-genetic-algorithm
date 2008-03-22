from individual import Individual
from helperfuncs import lcs, bitHamming as hamming

class Test:
    def __init__(self, params, random):
        self.random = random
        self.geneLen = params['bits']

    def createPop(self, popsize):
        pop = [Individual(self.random, self.geneLen) for i in xrange(0, popsize)]
        return pop

    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is [best,worst]
        '''
        best,worst = user_feedback
        sumValue = 0
        print 'ind ', ind
        print 'user_feedback', user_feedback
        if ind.genome == best.genome:
            sumValue = 2 * len(ind.genome)
        elif ind.genome == worst.genome:
            sumValue = 0
        else:
            #sumValue += lcs(ind.genome, best.genome)
            #sumValue += len(ind.genome)-lcs(ind.genome, worst.genome)
            sumValue += hamming(ind, best, worst)

        ind.scalefit = ind.fitness = sumValue


    def scaleFitness(self, pop):
        pass


    def draw(self, parentPanel, subset, population):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        import panel.plot_individual as _individual

        data_max = len(population.pop[0].genome)
        panels = []
        # Print individuals, number to display is specified in options dialog
        for i in xrange(len(subset)):
            panels.append(_individual.IndividualPanel(parentPanel, i, sum(subset[i].genome), data_max))

        return panels

            
    def report(self, pop, gen):
        maxFit = 0.0
        sumFit = 0.0
        for ind in pop:
            if ind.fitness > maxFit:
                maxFit = ind.fitness
                best = ind
            sumFit += ind.fitness
            
        print '%i) Best Fit: %.2f, Avg Fit: %.2f' % (gen, best.fitness, sumFit/len(pop))


    def test(self, pop):
        print 'Test'
