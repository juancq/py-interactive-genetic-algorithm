import app.maskapp as maskapp
from app.helperfuncs import ham
import openglpanel as gl


class Maskglapp(maskapp.MaskApplication):
    def __init__(self, params, random):
        maskapp.MaskApplication.__init__(self, params, random)


#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is a list of the user's input,
        the list contents are ordered the same as the 
        feedback variable in the config yaml file.
        [best]
        '''
        # needs to be rewritten
        best = user_feedback[0]
        subj = 0
        for attr_name, chrom in ind.genome.iteritems():
            if chrom:
                subj += ham(best.genome[attr_name], chrom)
        ind.scalefit = ind.fitness = subj


#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        # example, creating empty panels to display
        panel = []
        for i in xrange(len(subset)):
            data = self.decode(subset[i])
            panel.append(gl.OpenGLPanel(parentPanel, i, data))
        return panel

#-------------------------------------------#
