import random as rnd
from gacommon import gaParams

class Parameters:
    def __init__(self, params):
        self.seed = params['seed']
        if self.seed:
            self.random = rnd.Random(self.seed)
        else:
            self.random = rnd.Random()
        self.numgen = params['numgen']
        self.crossover = Crossover(params['crossover'], self.random)
        self.mutate = Mutation(params['mutation'], self.random)

        app = params['application']
        appname = app['name']
        execstr = 'from app.%s.%s import %s as appclass' % (appname, appname, appname.capitalize())
        exec(execstr)
        self.app = appclass(app, self.random)

        poptype = params['population']['type']
        execstr = 'from population.%s import %s as popclass' % (poptype, poptype.capitalize())
        exec(execstr)
        self.pop = popclass(self, params['population'])

        self.params = params

class Crossover:
    def __init__(self, params, rand):
        self.random = rand
        self.points = params['points']

        funcname = params['type']
        execstr = 'from xo.%s import %s as func' % (funcname, funcname)
        exec(execstr)
        self._func = func

    def __call__(self, p1, p2):
        return self._func(p1, p2, gaParams.getVar('crossover_prob'), self.points, self.random)

class Mutation:
    def __init__(self, params, rand):
        self.params = params
        self.random = rand

        funcname = params['type']
        execstr = 'from mut.%s import %s as func' % (funcname, funcname)
        exec(execstr)
        self._mutation = func

    def __call__(self, ind):
        return self._mutation(ind, gaParams.getVar('mutation_prob'), self.params, self.random)

