def random(pop, genomes, random_mod, to_replace):
    popsize = len(pop) - 1
    genome_len = len(genomes)

    for i in xrange(to_replace):
        rand_index = random_mod.randint(0, popsize)
        pop[rand_index] = genomes[i%genome_len]
