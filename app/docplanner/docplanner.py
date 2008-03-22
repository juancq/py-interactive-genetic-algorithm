from iga.individual import Individual
from iga.gacommon import gaParams

import parseTree, decodePlan, blockmaker

import app.app as app

#-------------------------------------------#
class DocplanIndividual(Individual):
    def __init__(self, random, genome_len, genome):
        Individual.__init__(self, random, genome_len, genome)

        self.rank = 10
        self.crowded_distance = 0
        self.decoded_plan = None
        self.numRoom = None
        self.roomarea = None
        self.roomlist = None
        self.roomDesc = None
        self.roomSizes = None

    def __cmp__(self, other):
        return cmp(self.rank, other.rank)


#-------------------------------------------#
class Docplanner(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

        import time
        ltime = time.localtime()
        hour, min = ltime[3], ltime[4]
        self.fout = open('data/%s_pop_%d-%d' % (params['name'], hour, min), 'w')
        self.fout.write('gen\tobj\tsubj\t\ttop obj\ttop subj\tc1\tc2\tc3\tc4\tc5\n')

#-------------------------------------------#
    def createPop(self, popsize):        
        
        params = self.params
        random = self.random
        import createInd
        pop = []

        ## template individual
        #tree_genome = self.params['template']
        #new_ind = DocplanIndividual(self.random, None, genome=tree_genome)
        #self.decodePlan(new_ind)
        #new_ind.rank = 1
        #new_ind.crowded_distance = 100
        #pop.append(new_ind)

        for i in xrange(popsize):
            tree_genome = createInd.createIndividual(random, params['maxDepth'], params['maxRoom'], params['minRoom'], params['num_shapes'])
            new_ind = DocplanIndividual(random, None, genome=tree_genome)
            self.decodePlan(new_ind)
            pop.append(new_ind)
        
        return pop
    
#-------------------------------------------#
    def decodePlan(self, ind):
        room_list = parseTree.parseTree(ind, self.params['plotSizeX'],self.params['plotSizeY'])
        plan = decodePlan.decodePlan(room_list['desc'], room_list['sizes'])

        ind.decoded_plan = plan
        ind.numRoom = plan[0]
        ind.roomarea = plan[1]
        ind.roomlist = plan[2]
        ind.roomDesc = plan[3]
        ind.roomSizes = plan[4]
        ind.transf = room_list['transf']

#-------------------------------------------#
    def roomDims(self, desc, size):

        dim = []
        for rooms in xrange(len(desc)):
            if desc[rooms] != 'S':
                length = size[rooms][2] - size[rooms][0]
                breadth = size[rooms][3] - size[rooms][1]
                dim.extend([desc[rooms], length, breadth])

        return dim

        
#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        '''
        self.decodePlan(ind)

        best = user_feedback[0]

        roomNum = ind.numRoom
        totArea = ind.roomarea
        SharedWalls = ind.roomlist
        roomNumBest = best.numRoom
        totAreaBest = best.roomarea
        SharedBest = best.roomlist

        fit = []
        Dimensions = self.roomDims(ind.roomDesc, ind.roomSizes)

        # 1.Number of rooms
        if roomNum == 0 or roomNum == 1 or roomNum > 8:
            fit.append(max(roomNumBest-2,8-roomNumBest)+1)
        else:
            fit.append(abs(roomNum - roomNumBest))

        # 2.Adjacency
        penalty = 0
        for rels in xrange(len(SharedWalls)):
            penalty = penalty + (SharedWalls[rels] - SharedBest[rels])**2
        fit.append(penalty)

        #---------------------------------------------
        # small helper func
        def room_append(dim, room_dim, descriptor):
            k = dim.index(descriptor)
            room_dim.extend([dim[k+1],dim[k+2]])
        #---------------------------------------------
        # small helper func 2
        def compute_penalty(room1, room2, dim1, dim2):
            penalty = 0.
            if room1 < room2:
                if room1 < dim1:
                    penalty = dim1 - room1
            else:
                if room2 < dim1:
                    penalty = dim1 - room2

            penalty1 = penalty/dim1

            penalty = 0.0
            if room1*room2 < dim2:
                penalty = dim2 - room1*room2

            penalty2 = penalty/dim2

            return penalty1, penalty2
        #---------------------------------------------

        # 3.NeufertGuide Rules
        if roomNum == 0 or roomNum == 1:
            fit.append(1.0)
            fit.append(1.0)
        else:
            penalty = 0.0
            penaltyOne = 0.0
            penaltyTwo = 0.0
            roomDim = []

            if roomNum == 2:
                room_append(Dimensions, roomDim, 'LBK')

                # Minimum dimension of LBK should be 20'10" and minimum area should be 300 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 104.2, 7500.0)

                fit.append(penaltyOne/104.2)
                fit.append(penaltyTwo/7500.0)

            elif roomNum == 3:
                room_append(Dimensions, roomDim, 'LKT')
                room_append(Dimensions, roomDim, 'BED')

                # Minimum dimension of LKT should be 19'10" and minimum area should be 270 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 99.2, 6750.0)

                # Minimum dimension of BED should be 9'4" and minimum area should be 120 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[2], roomDim[3], 46.7, 3000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                fit.append(penaltyOne/2.0)
                fit.append(penaltyTwo/2.0)

            elif roomNum == 4:
                room_append(Dimensions, roomDim, 'LKT')
                room_append(Dimensions, roomDim, 'MBR')
                room_append(Dimensions, roomDim, 'BED')

                # Minimum dimension of LKT should be 19'10" and minimum area should be 270 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 99.2, 6750.0)

                # Minimum dimension of MBR should be 9'4" and minimum area should be 120 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[2], roomDim[3], 46.7, 3000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp
                
                # Minimum dimension of BED should be 8' and minimum area should be 80 sq.ft
                pen1_temp, pen2_temp = compute_penalty(roomDim[4], roomDim[5], 40.0, 2000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                fit.append(penaltyOne/3.0)
                fit.append(penaltyTwo/3.0)

            elif roomNum == 5:
                room_append(Dimensions, roomDim, 'LIV')
                room_append(Dimensions, roomDim, 'MBR')
                room_append(Dimensions, roomDim, 'BED')
                    
                # Minimum dimension of LIV should be 11'6" and minimum area should be 160 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 57.5, 4000.0)

                # Minimum dimension of MBR should be 9'4" and minimum area should be 120 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[2], roomDim[3], 46.7, 3000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                # Minimum dimension of BED should be 8' and minimum area should be 80 sq.ft
                pen1_temp, pen2_temp = compute_penalty(roomDim[4], roomDim[5], 40.0, 2000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                fit.append(penaltyOne/3.0)
                fit.append(penaltyTwo/3.0)
                
            elif roomNum == 6:
                room_append(Dimensions, roomDim, 'LIV')
                room_append(Dimensions, roomDim, 'MBR')
                room_append(Dimensions, roomDim, 'DIN')
                room_append(Dimensions, roomDim, 'BED')
                    
                # Minimum dimension of LIV should be 11'6" and minimum area should be 160 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 57.5, 4000.0)

                # Minimum dimension of MBR should be 9'4" and minimum area should be 120 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[2], roomDim[3], 46.7, 3000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                # Minimum dimension of DIN should be 8'4" and minimum area should be 100 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[4], roomDim[5], 41.7, 2500.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                # Minimum dimension of BED should be 8' and minimum area should be 80 sq.ft
                pen1_temp, pen2_temp = compute_penalty(roomDim[6], roomDim[7], 40.0, 2000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp
                
                fit.append(penaltyOne/4.0)
                fit.append(penaltyTwo/4.0)

            else:
                room_append(Dimensions, roomDim, 'LIV')
                room_append(Dimensions, roomDim, 'MBR')
                room_append(Dimensions, roomDim, 'DIN')
                room_append(Dimensions, roomDim, 'BED')
                room_append(Dimensions, roomDim, 'GBR')
                
                # Minimum dimension of LIV should be 11'6" and minimum area should be 170 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 57.5, 4250.0)

                # Minimum dimension of MBR should be 9'4" and minimum area should be 120 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[2], roomDim[3], 46.7, 3000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                # Minimum dimension of DIN should be 8'4" and minimum area should be 110 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[4], roomDim[5], 41.7, 2750.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                # Minimum dimension of BED should be 8' and minimum area should be 80 sq.ft
                pen1_temp, pen2_temp = compute_penalty(roomDim[6], roomDim[7], 40.0, 2000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp
            
                # Minimum dimension of GBR should be 8' and minimum area should be 80 sq.ft
                pen1_temp, pen2_temp = compute_penalty(roomDim[8], roomDim[9], 40.0, 2000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                fit.append(penaltyOne/5.0)
                fit.append(penaltyTwo/5.0)
        
        # 4.Total Built Area
        if roomNum == 0 or roomNum == 1:
            fit.append(1.0)
        else:
            penalty = 0.0
            if sum(totArea) < sum(totAreaBest):
                penalty = (sum(totAreaBest) - sum(totArea))/sum(totAreaBest)

            fit.append(penalty)
            
        ind.fitness = fit


#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panels = []
        for ind in subset:
            doc = blockmaker.BlockMaker(parentPanel, dimensions=ind.roomSizes, description=ind.roomDesc, transf = ind.transf)
            panels.append(doc)

        return panels


#-------------------------------------------#
    def paramSpace(self, pop, user_selected):
        best = user_selected[0]
        objmax = [max(best.numRoom-2, 8-best.numRoom)+1., 5., 1.0, 1.0, 1.0]
        objmin = [0., 0., 0.0, 0.0, 0.0]

        self.limits = {'max': objmax, 'min': objmin}

        return objmax, objmin


#-------------------------------------------#
    def report(self, pop, subset, gen):
        '''
        Write to console or file
        population statistics.
        '''
        # minus fitness bias dimension
        len_fit = len(pop[0].fitness) - 1
        fit = [0.] * len_fit
        top_fit = [0.] * len_fit
        sub_len = len(subset)

        for ind in pop:
            for i in xrange(len_fit):
                fit[i] += (ind.fitness[i] - self.limits['min'][i])/ self.limits['max'][i] * 100.

        for ind in subset:
            for i in xrange(len_fit):
                top_fit[i] += (ind.fitness[i] - self.limits['min'][i])/ self.limits['max'][i] * 100.


        pop_len = len(pop)
        data_str = '%d\t%.5f' % (gen, (fit[2]+fit[3])/float(pop_len))
        data_str += '\t%.5f' % ((fit[0]+fit[1]+fit[4])/float(pop_len))

        # print fitness of subset
        data_str += '\t%.5f' % ((top_fit[2]+top_fit[3])/float(sub_len))
        data_str += '\t%.5f' % ((top_fit[0]+top_fit[1]+top_fit[4])/float(sub_len))

        for i in xrange(len_fit):
            data_str += '\t%.5f' % (fit[i]/float(pop_len))

        self.fout.write(data_str + '\n')

#-------------------------------------------#
    def close(self):
        self.fout.close()

#-------------------------------------------#
