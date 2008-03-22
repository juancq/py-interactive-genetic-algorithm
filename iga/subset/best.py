def best(pop, rand, size):
    newpop = pop[:]
    newpop.sort()
    print 'newpop end ', newpop[-1].fitness, 'newpop begin', newpop[0].fitness
    subset = newpop[-size:]
    newindex = []
    for ind in subset:
        newindex.append(pop.index(ind))

    return subset, newindex
