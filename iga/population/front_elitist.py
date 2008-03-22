def front_elitist(oldPop, fronts):
    newPop = []

    popsize = len(oldPop)
    sols = 0
    i = 0
    while(sols <= popsize):
        sols += len(fronts[i])
        i += 1

    newPop = []
    for k in xrange(i-1):
        for j in xrange(len(fronts[k])):
            newPop.append(fronts[k][j])
    n = popsize-len(newPop)

    if (n != 0):
        fronts[i-1].sort(lambda a,b: cmp(a.crowded_distance, b.crowded_distance))
        newPop.extend(fronts[i-1][-n:])

    return newPop
