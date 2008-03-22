
def genLevel(random):
    randNum = random.random()
    count = 0

    # space
    if randNum < 0.20:
        randNum = 0.0
        splitter = 1
    # room
    elif randNum > 0.75:
        randNum = 1.0
        splitter = 1
    # something else
    else:
        splitter = random.randint(1,2)
        count = 1

    level = [splitter, randNum]
    return level, count

#-------------------------------------------#
def createIndividual(random, maxDepth, maxRoom, minRoom):

    flag = 0
    while(flag == 0):

        level, ctr = genLevel(random)
        tree = [level]
        Depth = 0

        while(ctr>0 and Depth<maxDepth):
            count = ctr
            ctr = 0
            tempTree = []
            for k in xrange(2*count):
                level, ctr_tmp = genLevel(random)
                ctr += ctr_tmp
                tempTree.append(level)
            Depth += 1
            tree.append(tempTree)


        roomCount = 0
        if (Depth > 1 and Depth < maxDepth):
            for k in xrange(1, len(tree)):
                for j in xrange(len(tree[k])):
                    # room
                    if tree[k][j][1] == 1.0:
                        roomCount += 1

            if roomCount > minRoom and roomCount < maxRoom:
                flag = 1

    return tree
