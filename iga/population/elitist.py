def indCmp(i1, i2):
    return cmp(i1.fitness, i2.fitness)

def elitist(oldPop, newPop):
    pop = []
    pop.extend(oldPop)
    pop.extend(newPop)
    pop.sort(indCmp, reverse=True)
    return pop[0:len(oldPop)]
