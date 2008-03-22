def roulette(pop, random):
    totalFitness = 0.0
    for ind in pop:
        totalFitness += ind.scalefit
    thresh = totalFitness * random.random()
    partSum = 0.0

    for ind in pop:
        partSum += ind.scalefit
        if partSum >= thresh:
            return ind
    return ind #If we never make it above the threshold, return last ind
