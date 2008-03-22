from app.helperfuncs import lcs, bitHamming as hamming
import app.app as app
from gamepanel import GamePanel

class Frogger(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)
        self.geneLen = params['bits']

#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panels = []
        for i in xrange(len(subset)):
            panels.append(GamePanel(parentPanel, i))

        return panels

            
#-------------------------------------------#
