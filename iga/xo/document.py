import copy

def createPosList(k, random):

    pzero = [ [0]*len(k[i]) for i in xrange(len(k)) ]

    a = random.randint(0, len(k)-1)
    b = random.randint(0, len(k[a])-1)

    flag = 0
    
    pzero[a][b] = 1
    while (flag == 0):
        for i in xrange(sum(pzero[a])):
            if k[a][b+i][1] == 1.0 or k[a][b+i][1] == 0.0:
                pass
            else:
                ctr = 0
                for j in xrange(b+i):
                    if k[a][j][1] == 1.0 or k[a][j][1] == 0.0:
                        pass
                    else:
                        ctr = ctr + 1
                pzero[a+1][2*ctr] = 1
                pzero[a+1][2*ctr+1] = 1
                #print pzero
                
        a = a+1
        if a == len(k):
            flag = 1
            break
        elif sum(pzero[a]) == 0:
            flag = 1
            break
        else:  
            b = pzero[a].index(1)

    return pzero

def extractTree(k, pos):

    extractedTree = []
    for i in xrange(len(pos)):
        level = []
        for j in xrange(len(pos[i])):
            if pos[i][j] == 1:
                level.append(k[i][j])
        if level != []:
            extractedTree.append(level)

    return extractedTree


def cross(child,pos,extTree):

    flag = 0
    # 1) In pos go to the first "1" position, delete the corresponding entry in child and replace by first entity in extTree
    for i in xrange(len(pos)):
        if sum(pos[i]) != 0:
            j = pos[i].index(1)
            break

    del child[i][j]
    child[i].insert(j,extTree[0][0])

    # 2) In pos, after the first "1" position, find all other "1" positions and delete corresponding entries in child
    for k in xrange(i+1,len(pos)):
        count = 0
        for l in xrange(len(pos[k])):
            if pos[k][l] == 1:
                count = count+1
                if count == 1:
                    del child[k][l]
                else:
                    del child[k][l-count+1]

    k = 1
    
    # 3) starting inserting extTree into child
    while (flag == 0):
        # does extTree[k] exist?
        if len(extTree) > k:                     # does exist
            # does child[i+1] exist?
            if len(child) <= i+1:                # does not exist
                # create child[i+1] by appending [] to child
                child.append([])

            # in child[i] find number of positions before j where child[i][][1] > 0.0 and < 1.0
            ctr = 0
            for l in xrange(j):
                if child[i][l][1] == 1.0 or child[i][l][1] == 0.0:
                    pass
                else:
                    ctr = ctr + 1

            for l in xrange(len(extTree[k])):
                child[i+1].insert(2*ctr+l,extTree[k][l])

            j = 2*ctr
            i = i+1
            k = k+1
        else:
            flag = 1

    # 4) clean up child - delete any empty lists that may exist in child
    emptyCheck = 0
    i = 0
    length = len(child)
    while (emptyCheck < length):
        if child[i] == []:
            del child[i]
        else:
            i = i+1
        emptyCheck = emptyCheck + 1

    return child

def countLeaves(genome):
    count = 0
    for node in genome:
        if type(node[0]) is list:
            count += countLeaves(node)
        else:
            if node[1] == 1.0 or node[1] == 0.0:
                count += 1
    return count
                

def setInherit(c1, c2, c1_from_p1, c2_from_p1, p1Len, p2Len):
    c1.from_p1 = c1_from_p1/float(p1Len)
    c1.from_p2 = 1. - c1.from_p1

    c2.from_p1 = c2_from_p1/float(p2Len)
    c2.from_p2 = 1. - c2.from_p1


def document(p1, p2, prob, points, random):

    if random.random() < prob:
        
        c1Genome = copy.deepcopy(p1.genome['tree'][1:])
        c2Genome = copy.deepcopy(p2.genome['tree'][1:])

        pos1 = createPosList(c1Genome, random)
        pos2 = createPosList(c2Genome, random)
    
        # extract subtrees
        extTree1 = extractTree(c1Genome,pos1)
        extTree2 = extractTree(c2Genome,pos2)

        ext1Leaves = countLeaves(extTree1)
        ext2Leaves = countLeaves(extTree2)
        p1Leaves = countLeaves(c1Genome)
        p2Leaves = countLeaves(c2Genome)
        from_p1 = p1Leaves - ext1Leaves
        from_p2 = p2Leaves - ext2Leaves

        k1 = cross(c1Genome,pos1,extTree2)
        k2 = cross(c2Genome,pos2,extTree1)
        k1Leaves = countLeaves(k1)
        k2Leaves = countLeaves(k2)


        if not(k1Leaves == from_p1+ext2Leaves and k2Leaves == from_p2+ext1Leaves):
            print 'Error!!'

        k1.insert(0, p1.genome['tree'][0])
        k2.insert(0, p2.genome['tree'][0])

        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome['tree'] = k1
        c2.genome['tree'] = k2

        c1.from_p1 = from_p1/float(k1Leaves)
        c1.from_p2 = 1. - c1.from_p1

        c2.from_p2 = from_p2/float(k2Leaves)
        c2.from_p1 = 1. - c2.from_p2

        #setInherit(c1, c2, from_p1, k2Leaves-from_p2, k1Leaves, k2Leaves)

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)
