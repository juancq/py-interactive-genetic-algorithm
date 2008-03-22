def nsgafronts(pop, rand, size):
    newpop = pop[:]
    newpop.sort(lambda a,b: cmp(a.rank, b.rank))
    subset = newpop[:size]
    newindex = []
    for ind in subset:
        newindex.append(pop.index(ind))
    return subset, newindex
