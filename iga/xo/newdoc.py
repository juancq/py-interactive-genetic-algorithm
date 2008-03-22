import copy

def newdoc(p1, p2, prob, points, random):

    if random.random() < prob:
        
        c1Genome = copy.deepcopy(p1.genome['tree'])
        c2Genome = copy.deepcopy(p2.genome['tree'])

        # operator 5 - add random shape
        #c1Genome.addNode()
        #c2Genome.addNode()

        # operator 4 - delete random shape
        #c1Genome.deleteNode()
        #c2Genome.deleteNode()

        # operator 3 - clone an existing shape and add to another branch
        #c1Genome.cloneNode()
        #c2Genome.cloneNode()

        # quad tree, so pick between 0 and 4
        b1, b2 = random.sample(range(0, 4), 2)
        
        branch1 = c1Genome.branch[b1][:]
        branch2 = c2Genome.branch[b2][:]
        c1Genome.branch[b1] = branch2
        c2Genome.branch[b2] = branch1

        # operator 1
        #b1_centers = [i.getCenter() for i in branch1]
        #b2_centers = [i.getCenter() for i in branch2]
        #c1Genome.quadrantSwap(b1, b1_centers)
        #c2Genome.quadrantSwap(b2, b2_centers)
        #print 'centers', b1_centers, b2_centers

        # operator 2
        c1Genome.rearrange()
        c2Genome.rearrange()


        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome['tree'] = c1Genome
        c2.genome['tree'] = c2Genome

    else:
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)

    return (c1, c2)
