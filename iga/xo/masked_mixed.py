import copy

def setInherit(c1, c2, c1_from_p1, c2_from_p1, p1Len, p2Len):
    c1.from_p1 = c1_from_p1/float(p1Len)
    c1.from_p2 = 1. - c1.from_p1

    c2.from_p1 = c2_from_p1/float(p2Len)
    c2.from_p2 = 1. - c2.from_p1


def simple(c1, c2, xopt):
    _c1 = c1[:xopt] + c2[xopt:]
    _c2 = c2[:xopt] + c1[xopt:]
    return _c1, _c2

def pmx(c1, c2, left, right):
    c1Grid = c1[:]
    c2Grid = c2[:]
    for i in xrange(left, right+1):
        fal = c2.index(c1[i])

        # Swap child 2 bits
        temp = c2Grid[fal]
        c2Grid[fal] = c2Grid[i]
        c2Grid[i] = temp

        fal = c1.index(c2[i])
        # Swap child 1 bits
        temp = c1Grid[fal]
        c1Grid[fal] = c1Grid[i]
        c1Grid[i] = temp

    return c1Grid, c2Grid


def masked_mixed(p1, p2, prob, points, random):
    if random.random() < prob:

        common = []
        onlyp1 = []
        onlyp2 = []

        for attr_name, attr_dict in p1.genome.iteritems():
            # if attr is also on other individual and it's not masked
            if attr_dict:
                if p2.genome.has_key(attr_name) and p2.genome[attr_name]:
                    common.append(attr_name)
                else:
                    onlyp1.append(attr_name)

        for attr_name, attr_dict in p2.genome.iteritems():
            # if attr is also on other individual and it's not masked
            if attr_dict:
                if not (p1.genome.has_key(attr_name) and p1.genome[attr_name]):
                    onlyp2.append(attr_name)


        c1Genome = p1.genome.copy()
        c2Genome = p2.genome.copy()
        for attr_name in common:
            if attr_name is 'style':
                xopt = random.randint(0, len(p1.genome[attr_name])-1)
                c1Genome[attr_name], c2Genome[attr_name] = simple(p1.genome[attr_name], p2.genome[attr_name], xopt)
            elif attr_name is 'grid':
                geneLen = len(p1.genome['grid'])
                left = random.randrange(1, geneLen - 2)
                right = random.randrange(left, geneLen - 1)
                c1Genome[attr_name], c2Genome[attr_name] = pmx(p1.genome[attr_name], p2.genome[attr_name], left, right)


        for attr_name in onlyp1:
            c1Genome[attr_name] = p1.genome[attr_name]

        for attr_name in onlyp2:
            c2Genome[attr_name] = p2.genome[attr_name]

        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome = c1Genome
        c2.genome = c2Genome
        #setInherit(c1, c2, c1_from_p1, c2_from_p1, geneLen, geneLen)

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)
