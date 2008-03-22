#-------------------------------------------#
def hamming(chrom1, chrom2):
    sumValue = 0
    size = min(len(chrom1), len(chrom2))
    for i in xrange(size):
        if chrom1[i] == chrom2[i]:
            sumValue += 1

    return sumValue


#-------------------------------------------#
def bitHamming(ind, best, worst = None):
    sumValue = 0
    if worst:
        for i in xrange(len(ind.genome)):
            if ind.genome[i] == best.genome[i]:
                sumValue += 1
            if not (ind.genome[i] == worst.genome[i]):
                sumValue += 1
    else:
        for i in xrange(len(ind.genome)):
            if ind.genome[i] == best.genome[i]:
                sumValue += 1

    return sumValue


#-------------------------------------------#
def ham(best, ind):
    sum_value = 0
    for i in xrange(len(best)):
        if ind[i] == best[i]:
            sum_value += 1
    return sum_value

#-------------------------------------------#
def lcs(x, y):
    m = len(x)
    n = len(y)

    c = [[0]*(n+1)]*(m+1)

    for i in xrange(1, m+1):
        for j in xrange(1, n+1):
            if x[i-1] == y[j-1]:
                c[i][j] = c[i-1][j-1] + 1
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
            else:
                c[i][j] = c[i][j-1]

    return c[-1][-1]

#-------------------------------------------#
