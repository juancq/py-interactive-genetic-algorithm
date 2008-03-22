import copy

def setInherit(c1, c2, c1_from_p1, c2_from_p1, p1Len, p2Len):
    c1.from_p1 = c1_from_p1/float(p1Len)
    c1.from_p2 = 1. - c1.from_p1

    c2.from_p1 = c2_from_p1/float(p2Len)
    c2.from_p2 = 1. - c2.from_p1


def masked(p1, p2, prob, points, random):
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
            xopt = random.randint(0, len(p1.genome[attr_name])-1)
            c1Genome[attr_name] = p1.genome[attr_name][:xopt] + p2.genome[attr_name][xopt:]
            c2Genome[attr_name] = p2.genome[attr_name][:xopt] + p1.genome[attr_name][xopt:]

        print 'only p1 ', onlyp1
        print 'only p2 ', onlyp2
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
