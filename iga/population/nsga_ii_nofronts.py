import copy
import standard

class Nsga_ii(standard.Standard):
    def __init__(self, paramClass, paramDict):
        standard.Standard.__init__(self, paramClass, paramDict)

#---------------------------------------#
    def crowdedDistance(self, fronts):
        '''
        Compute the crowding distance of individuals
        based on which front they're located.
        '''
        objmax, objmin = self.params.app.paramSpace(self.popsize, self.user_selected)
        #objmax.append(1.0)
        #objmin.append(0.0)

        numFronts = len(fronts)
        for i in xrange(numFronts):

            # for each criteria
            for k in xrange(len(objmax)):
            
                extFitness = [fronts[i][j].fitness[k] for j in xrange(len(fronts[i]))]
                    
                best_index = extFitness.index(min(extFitness))
                worst_index = extFitness.index(max(extFitness))

                for j in xrange(len(fronts[i])):
                    crowded_dist = 0.0
                    if j == best_index or j == worst_index:
                        crowded_dist = 1.0e3000
                    else:
                        crowfit = []
                        for l in xrange(len(fronts[i])):
                            crowfit.append(extFitness[j] - extFitness[l])
                        sortedcrowfit = copy.deepcopy(crowfit)
                        sortedcrowfit.sort()
                        zero_index = sortedcrowfit.index(0)
                        
                        more_index = crowfit.index(sortedcrowfit[zero_index-1])
                        less_index = crowfit.index(sortedcrowfit[zero_index+1])

                        crowded_dist = (float(extFitness[more_index] - extFitness[less_index])/float(objmax[k] - objmin[k]))

                    fronts[i][j].crowded_distance += crowded_dist

#---------------------------------------#
    def domination(self, a, b):
        '''
        Determine if either a or b dominates the other.
        '''
        compare = []
        criteria = len(a)

        for i in xrange(criteria):
            if a[i] < b[i]:
                compare.append(1)
            elif a[i] == b[i]:
                compare.append(0)
            else:
                compare.append(-1)

        if max(compare) > 0 and min(compare) >= 0:
            compareCt = 1
        elif max(compare) <= 0 and min(compare) < 0:
            compareCt = 2
        else:
            compareCt = 0

        return compareCt
    
#---------------------------------------#
    def createFronts(self, pop):
        '''
        Create non-dominated fronts from evaluated population.
        '''
        # create fronts
        fit = [ind.fitness for ind in pop]
        serial = range(len(pop))

        nonDomFronts = []
        while (len(fit) > 0):
            nonDomPop = [0]
            i = 1
            flag = 0
            while (i < len(fit)):
                domCt = []
                nonDomCt = 0
                flag = 0
                for k in xrange(len(nonDomPop)):
                    compareCount = self.domination(fit[i], fit[nonDomPop[k]])
                    if compareCount == 1:
                        #i dominates
                        domCt.append(k)
                    elif compareCount == 2:
                        #i is dominated
                        i += 1
                        flag = 1
                        break
                    else:
                        #no domination
                        nonDomCt += 1

                if flag == 0:
                    if nonDomCt == k+1:
                        nonDomPop.append(i)
                    if len(domCt) > 0:
                        for k in xrange(len(domCt)):
                            domCt[k] = domCt[k] - k
                        for k in xrange(len(domCt)):
                            del nonDomPop[domCt[k]]

                        nonDomPop.append(i)
                    i += 1

            nonDomPop.sort()
            front = []
            for k in xrange(len(nonDomPop)):
                del fit[nonDomPop[k]-k]
                ind_index = serial[nonDomPop[k]]
                pop[ind_index].crowded_distance = 0.
                pop[ind_index].rank = len(nonDomFronts)+1
                front.append(pop[ind_index])

            nonDomFronts.append(front)
            for k in xrange(len(nonDomPop)):
                del serial[nonDomPop[k]-k]

        return nonDomFronts

#---------------------------------------#
    def fitnessBias(self, pop):
        for ind in pop:
            bias = ind.bloodline
            for i in xrange(len(ind.fitness)):
                ind.fitness[i] += ind.fitness[i] * (1.-bias)

            #ind.fitness.append(1.-bias)

        #for ind in pop:
        #    bias = ind.bloodline
        #    ind.fitness.append(1.-bias)

#---------------------------------------#
    def nextgen(self):
        '''
        Create next generation from current population.
        '''
        newPop = []
        random = self.params.random

        for i in xrange(0, self.popsize, 2):
            p1 = self.pop[i]
            p2 = self.pop[i+1]
            c1, c2 = self.crossover(p1, p2)
            self.params.mutate(c1)
            self.params.mutate(c2)
            newPop.extend([c1,c2])

        # evaluate children
        self.eval(newPop)
        self.pop = newPop

#---------------------------------------#
