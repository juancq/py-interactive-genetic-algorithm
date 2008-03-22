#!/usr/bin/env python

import random

def genLevel():
    randNum = random.random()
    level = []
    count = 0
    if randNum < 0.20:
        randNum = 0.0
        splitter = 1
    elif randNum > 0.75:
        randNum = 1.0
        splitter = 1
    else:
        splitter = random.randint(1,2)
        count = 1

    level.append(splitter)
    level.append(randNum)
    level.append(count)
    
    return level

def createIndividual(maxDepth, maxRoom, minRoom):

    flag = 0

    while(flag == 0):

        tree,level,count = [], [], []
        level = genLevel()
        ctr=sum(level[-1:])

        tree.append(level[:-1])
        level = []
        Depth = 0

        while(ctr>0 and Depth<maxDepth):
            count = ctr
            ctr = 0
            tempTree = []
            for k in xrange(2*count):
                level = genLevel()
                ctr = ctr + sum(level[-1:])
                tempTree.append(level[:-1])
                level = []
            Depth = Depth + 1
            tree.append(tempTree)


        roomCount = 0
        if (Depth > 1 and Depth < maxDepth):
            for k in xrange(1,len(tree)):
                for j in xrange(len(tree[k])):
                    if tree[k][j][1] == 1.0:
                        roomCount = roomCount + 1

            if roomCount > minRoom and roomCount < maxRoom:
                flag = 1

    #print "FINAL TREE:", tree
    #print "FINAL DEPTH:", Depth

    return tree
