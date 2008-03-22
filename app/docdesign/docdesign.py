
import app.app as app
from app.helperfuncs import hamming,lcs
from iga.individual import Individual

import wx
import docpanel

#-------------------------------------------#
class DocIndividual(Individual):
    def __init__(self, random, genome_len, genome = None):
        Individual.__init__(self, random, genome_len, genome)
        self.rank = 0

    def __cmp__(self, other):
        return cmp(self.rank, other.rank)

#-------------------------------------------#
class Docdesign(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)
        num_img = len(params['images'])

        # clone attributes for each image
        new_attr = {}
        for i in xrange(num_img):
            for name,value in self.attr.iteritems():
                new_attr[name + ('_%d' % i)] = value

        self.attr = new_attr
        self.geneLen *= num_img

#-------------------------------------------#
    def createPop(self, popsize):
        pop = [DocIndividual(self.random, self.geneLen) for i in xrange(popsize)]
        return pop

#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is a list of the user's input,
        the list contents are ordered the same as the 
        feedback variable in the config yaml file.
        [best]
        '''
        ind.fitness = lcs(ind.genome, best.genome)

#-------------------------------------------#
    def draw(self, parent, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panel = []
        # example, creating empty panels to display
        i = 0
        for ind in subset:
            decoded_data = self.decode(ind)
            panel.append(docpanel.DocMaker(parent, i, decoded_data))
            i += 1
        return panel

#-------------------------------------------#

