    def report(self, pop, gen):
        '''
        Write to console or file
        population statistics.
        '''
        score = 0.
        for i in xrange(len(pop[0].fitness)):
            score += (pop[0].fitness[i] - self.limits['min'][i])/ self.limits['max'][i]
        max_score = score
        min_score = score
        max_ind = pop[0]
        min_ind = pop[0]
        avg_score = 0.

        for ind in pop:
            score = 0.
            for i in xrange(len(ind.fitness)):
                score += (ind.fitness[i] - self.limits['min'][i])/ self.limits['max'][i]
            avg_score += score

            if score > max_score:
                max_score = score
                max_ind = ind
            elif score < min_score:
                min_score = score
                min_ind = ind


        self.fout.write('%d  %.3f  %.3f  %.3f \n' % (gen, min_score, 
                                                avg_score/len(pop), max_score))
