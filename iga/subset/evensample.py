def evensample(pop, rand, size):
    newpop = pop[:]
    newpop.sort(key=lambda x:x.fitness)
    subset = []

    popsize = len(pop)
    step = popsize/size
    i = 0
    while i < popsize and len(subset) < size:
        subset.append(newpop[i])
        i += step

    newindex = []
    for ind in subset:
        newindex.append(pop.index(ind))

    return subset, newindex
    
