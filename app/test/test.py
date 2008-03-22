#from iga.individual import Individual
from app.helperfuncs import lcs, bitHamming as hamming
import app.app as app

class Test(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)
        self.geneLen = params['bits']

#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is [best,worst]
        '''
        best, worst = user_feedback
        sumValue = 0
        if ind.genome == best.genome:
            sumValue = 2 * len(ind.genome)
        elif ind.genome == worst.genome:
            sumValue = 0
        else:
            #sumValue += lcs(ind.genome, best.genome)
            #sumValue += len(ind.genome)-lcs(ind.genome, worst.genome)
            sumValue += hamming(ind, best, worst)

        ind.scalefit = ind.fitness = sumValue


#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        import plot as _individual
        data_max = len(subset[0].genome)
        panels = []
        # Print individuals, number to display is specified in options dialog
        for i in xrange(len(subset)):
            panels.append(_individual.PlotPanel(parentPanel, i, sum(subset[i].genome), data_max))

        return panels

            
#-------------------------------------------#
    def report(self, pop, gen):

        best = max(pop)
        sumFit = reduce(lambda a,b: a + b.fitness, pop, 0)
            
        print '%i) Best Fit: %.2f, Avg Fit: %.2f' % (gen, best.fitness, sumFit/len(pop))


#-------------------------------------------#
