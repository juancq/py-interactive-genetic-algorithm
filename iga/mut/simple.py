def simple(ind, prob, params, random):
    for i in xrange(len(ind.genome)):
        if random.random() < prob:
            ind.genome[i] = ind.genome[i] ^ 1
