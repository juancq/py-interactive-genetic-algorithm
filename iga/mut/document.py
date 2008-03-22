def simple_mut(random, prob, chrom):
    for i in xrange(len(chrom)):
        if random.random() < prob:
            chrom[i] ^= 1

def document(ind, prob, params, random):
    tree = ind.genome['tree']
    if random.random() < prob:
        tree[0][1] = 1.0 - tree[0][1]
        if not(tree[0][1] == 0.0 or tree[0][1] == 1.0):
            tree[0][0] = 3 - tree[0][0]

    for i in xrange(1, len(tree)):
        for j in xrange(len(tree[i])):
            if random.random() < prob:
                tree[i][j][1] = 1.0 - tree[i][j][1]
                if not(tree[i][j][1] == 0.0 or tree[i][j][1] == 1.0):
                    tree[i][j][0] = 3 - tree[i][j][0]

                else:

                    # mutate x
                    scale = tree[i][j][2]
                    simple_mut(random, prob, scale)

                    # mutate y
                    scale = tree[i][j][3]
                    simple_mut(random, prob, scale)

                    # mutate shape
                    if random.random() < prob:
                        tree[i][j][4] = tree[i][j][4] + random.randrange(1, 4) % 3 + 1


    # mutate color
    color = ind.genome['color']
    simple_mut(random, prob, color)
