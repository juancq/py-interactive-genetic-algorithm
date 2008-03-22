import copy
def bottom(pop, genomes, random_mod, to_replace):
    pop.sort()
    genome_len = len(genomes)

    for i in xrange(to_replace):
        pop[i] = copy.deepcopy(genomes[i%genome_len])
