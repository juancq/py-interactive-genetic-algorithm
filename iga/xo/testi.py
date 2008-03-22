import random

x = [0]*20
y = [1]*20

points = 2
genlen = 20
xoPoints = list(set([random.randint(0, genlen-1) for i in xrange(points)]))
xopts = xoPoints[:]
xoPoints.sort(reverse=True)
xopts.sort()

swapPoint = xoPoints.pop()
swap = False
c1Genome, c2Genome = [], []
c1_from_p1 = 0
c2_from_p1 = 0
for i in xrange(0, genlen):
    if i == swapPoint:
        swap = not swap
        if len(xoPoints) > 0:
            swapPoint = xoPoints.pop()
    if swap:
        c2_from_p1 += 1
        c2Genome.append(x[i])
        c1Genome.append(y[i])
    else:
        c1_from_p1 += 1
        c1Genome.append(x[i])
        c2Genome.append(y[i])


print 'c1genome and c2genome'
print c1Genome
print c2Genome

print xopts


c1 = []
c2 = []

beg = 0
swap = False
for pt in xopts:
    print 'beg and pt', beg, pt
    if swap:
        c1.extend(x[beg:pt])
        c2.extend(y[beg:pt])
        print 'hi'
    else:
        c1.extend(y[beg:pt])
        c2.extend(x[beg:pt])
        print 'here'
    beg = pt
    swap = not swap
c1.extend(x[beg:])
c2.extend(y[beg:])

print 'new c1 c2'
print c1
print c2
