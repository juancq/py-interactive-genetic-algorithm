def masked_mixed(ind, prob, params, random):
    if ind.genome['style']:
        for i in xrange(0, len(ind.genome['style'])):
            if random.random() < prob:
                ind.genome['style'][i] = ind.genome['style'][i] ^ 1

    if ind.genome['grid']:
        for i in xrange(0, len(ind.genome['grid'])):
            if random.random() < prob:
                swapIndex = random.randint(0, len(ind.genome['grid'])-1)
                temp = ind.genome['grid'][i]
                ind.genome['grid'][i] = ind.genome['grid'][swapIndex]
                ind.genome['grid'][swapIndex] = temp
