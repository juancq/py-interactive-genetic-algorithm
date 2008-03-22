import copy

def setInherit(c1, c2, c1_from_p1, c2_from_p1, p1Len, p2Len):
    c1.from_p1 = c1_from_p1/float(p1Len)
    c1.from_p2 = 1. - c1.from_p1

    c2.from_p1 = c2_from_p1/float(p2Len)
    c2.from_p2 = 1. - c2.from_p1


def mixed(p1, p2, prob, points, random):
    if random.random() < prob:
        geneLen = len(p1.genome['style'])
        # create a list of unique xo points
        xoPoints = list(set([random.randint(0, geneLen-1) for i in xrange(points)]))
        xoPoints.sort(reverse=True)

        swapPoint = xoPoints.pop()
        swap = False
        c1Genome = []
        c2Genome = []
        c1_from_p1 = 0
        c2_from_p1 = 0
        for i in xrange(0, geneLen):
            if i == swapPoint:
                swap = not swap
                if xoPoints: swapPoint = xoPoints.pop()

            if swap:
                c2_from_p1 += 1
                c2Genome.append(p1.genome['style'][i])
                c1Genome.append(p2.genome['style'][i])
            else:
                c1_from_p1 += 1
                c1Genome.append(p1.genome['style'][i])
                c2Genome.append(p2.genome['style'][i])

     
        # pmx  on grid chromosome
        geneLen = len(p1.genome['grid'])
        left = random.randrange(1, geneLen - 2)
        right = random.randrange(left, geneLen - 1)

        c1Grid = p1.genome['grid'][:]
        c2Grid = p2.genome['grid'][:]
        for i in xrange(left, right+1):
            fal = p2.genome['grid'].index(p1.genome['grid'][i])

            # Swap child 2 bits
            temp = c2Grid[fal]
            c2Grid[fal] = c2Grid[i]
            c2Grid[i] = temp

            fal = p1.genome['grid'].index(p2.genome['grid'][i])
            # Swap child 1 bits
            temp = c1Grid[fal]
            c1Grid[fal] = c1Grid[i]
            c1Grid[i] = temp


        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome = {'grid':c1Grid, 'style':c1Genome}
        c2.genome = {'grid':c2Grid, 'style':c2Genome}
        geneLen = len(p1.genome['style'])
        setInherit(c1, c2, c1_from_p1, c2_from_p1, geneLen, geneLen)

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)
