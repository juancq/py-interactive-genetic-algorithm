from copy import deepcopy

def setInherit(c1, c2, c1_from_p1, c2_from_p1, p1Len, p2Len):
    c1.from_p1 = c1_from_p1/float(p1Len)
    c1.from_p2 = 1. - c1.from_p1

    c2.from_p1 = c2_from_p1/float(p2Len)
    c2.from_p2 = 1. - c2.from_p1


def simple(p1, p2, prob, points, random):
    genlen = len(p1.genome)
    if random.random() < prob:
        xoPoints = list(set([random.randint(0, genlen-1) for i in xrange(points)]))
        xoPoints.sort(reverse=True)

        swapPoint = xoPoints.pop()
        swap = False
        c1Genome, c2Genome = [], []
        c1_from_p1 = 0
        c2_from_p1 = 0
        for i in xrange(0, genlen):
            if i == swapPoint:
                swap = not swap
                if xoPoints: swapPoint = xoPoints.pop()

            if swap:
                c2_from_p1 += 1
                c2Genome.append(p1.genome[i])
                c1Genome.append(p2.genome[i])
            else:
                c1_from_p1 += 1
                c1Genome.append(p1.genome[i])
                c2Genome.append(p2.genome[i])

        c1 = deepcopy(p1)
        c2 = deepcopy(p2)
        c1.genome = c1Genome
        c2.genome = c2Genome

        setInherit(c1, c2, c1_from_p1, c2_from_p1, genlen, genlen)

    else:
        c1 = deepcopy(p1)
        c2 = deepcopy(p2)

    return (c1, c2)
