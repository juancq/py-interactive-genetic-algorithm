def crowded_tournament(fronts, random):
    '''
    Now: Create mating pool.
    Later: return single individual.
    '''
    mating_pool = []
    solPairs = []

    front1 = random.randint(0, len(fronts)-1)
    front2 = random.randint(0, len(fronts)-1)

    ind1_index = random.randint(0, len(fronts[front1])-1)
    ind2_index = random.randint(0, len(fronts[front2])-1)
    ind1 = fronts[front1][ind1_index]
    ind2 = fronts[front2][ind2_index]

    if ind1.rank < ind2.rank:
        return ind1
    elif ind1.rank > ind2.rank:
        return ind2
    else:
        if ind1.crowded_distance > ind2.crowded_distance:
            return ind1
        else:
            return ind2
