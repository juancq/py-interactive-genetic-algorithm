class Simple:
    def __init__(self, params, random):
        self.random = random
        self.prob = params['prob']

    def __call__(self, ind):
        for i in xrange(0, len(ind.genome)):
            if self.random.random() < self.prob:
                ind.genome[i] = ind.genome[i] ^ 1
    
