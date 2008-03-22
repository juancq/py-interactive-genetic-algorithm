def best(self, pop, rand, size):
    newpop = pop[:]
    newpop.sort()
    return newpop[-size:]
    
