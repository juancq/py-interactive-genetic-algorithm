def bestworst(pop, rand, size):
    newpop = pop[:]
    newpop.sort(key=lambda x:x.fitness)
    print 'here: ', newpop[0].fitness, newpop[-1].fitness
    subset = newpop[:size/2] + newpop[-size/2:]

    newindex = []
    for ind in subset:
        newindex.append(pop.index(ind))

    return subset, newindex
    
