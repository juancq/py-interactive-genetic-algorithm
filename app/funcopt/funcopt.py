import app.app as app
import math

#-------------------------------------------#
class Funcopt(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

#-------------------------------------------#
    def fitness(self, ind):
        '''
        Compute fitness.
        '''
        data = self.decode(ind)
        x, y = data['x'], data['y']
        ind.x, ind.y = x, y

        num = 1. + math.log(x**2. + 7*y**2. + 1.)
        denom = 1. + 3*x**2. + 2*y**2. - x*y + x

        #num = 1. + 3.*x - y
        #denom = 3 + x*x + y*y

        ind.fitness = num/denom

#-------------------------------------------#
    def report(self, pop, gen):

        best = max(pop)
        sumFit = reduce(lambda a,b: a + b.fitness, pop, 0)
            
        print '%i) Best Fit: %f - (%f, %f), Avg Fit: %f' % (gen, best.fitness, best.x, best.y, sumFit/len(pop))

#-------------------------------------------#
