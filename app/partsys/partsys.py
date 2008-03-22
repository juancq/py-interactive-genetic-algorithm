import app.app as app
from app.helperfuncs import bitHamming as hamming
import openglpanel as gl


class Partsys(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is a list of the user's input,
        the list contents are ordered the same as the 
        feedback variable in the config yaml file.
        [best]
        '''
        best = user_feedback[0]
        subj = 0
        if ind.genome == best.genome:
            subj = self.geneLen
        else:
            subj += hamming(ind, best)

        ind.scalefit = ind.fitness = subj

#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panels = []
        for i in xrange(len(subset)):
            data = self.decode(subset[i].genome)
            panels.append(gl.OpenGLPanel(parentPanel, i, data))
        return panels

#-------------------------------------------#
    def report(self, pop, gen):

        best = max(pop)
        sumFit = reduce(lambda a,b: a + b.fitness, pop, 0)
            
        print '%i) Best Fit: %.2f, Avg Fit: %.2f' % (gen, best.fitness, sumFit/len(pop))

#-------------------------------------------#
