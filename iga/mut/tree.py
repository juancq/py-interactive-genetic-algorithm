def tree(ind, prob, params, random):
    tree = ind.genome
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
