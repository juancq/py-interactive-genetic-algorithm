from parameters import Parameters
from gacommon import gaParams

class GA:
    def __init__(self, params_dict):
        params = Parameters(params_dict)
        self.params = params
        self.gen = 0

#---------------------------------------#
    def run(self):
        '''
        '''
        self.params.pop.eval()
        self.params.app.report(self.params.pop.pop, self.gen)
        gen = self.gen
        limit = self.params.params['numgen']
        while gen < limit:
            self.params.pop.nextgen()
            gen += 1
            self.params.app.report(self.params.pop.pop, gen)


#---------------------------------------#
    def updateMask(self, mask):
        self.params.app.updateMask(self.params.pop.pop, mask)

#---------------------------------------#
