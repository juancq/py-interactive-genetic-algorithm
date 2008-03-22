from iga.individual import Individual
from iga.gacommon import gaParams

import parseTree, decodePlan, docpanel
from app.helperfuncs import hamming,lcs

import app.app as app

import roomClassifier, sharedWalls
from copy import deepcopy
from shape import ShapeObject
from tree import Tree

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

    def isequal(self, other):
        if self.numRoom == other.numRoom and self.roomarea == other.roomarea and self.roomlist == other.roomlist and self.roomDesc == other.roomDesc and self.roomSizes == other.roomSizes:
            return True
        else:
            return False
                
        return cmp(self.rank, other.rank)

    def __cmp__(self, other):
        return cmp(self.rank, other.rank)


#-------------------------------------------#
class Doctemplate(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

        import time
        ltime = time.localtime()
        hour, min = ltime[3], ltime[4]
        self.fout = open('data/%s_pop_%d-%d' % (params['name'], hour, min), 'w')
        self.fout.write('gen\tobj\tsubj\t\ttop obj\ttop subj\tc1\tc2\tc3\tc4\tc5\n')


        # parse file with color schemes
        f = open('app/doctemplate/color_schemes')
        data = f.readlines()
        f.close()

        colors = []
        # each scheme has 4 colors
        # each color is stored in columns, hence awkard reading from file
        for i in xrange(0, len(data), 4):
            name = data[i].strip()
            new_color = [[], [], [], []]
            for j in xrange(3):
                nums = map(int, data[i+j+1].split()[1:])
                for k in xrange(4):
                    new_color[k].append(nums[k])
            colors.append(new_color)

        self.colors = colors

        self.best_saved = None

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

        import math
        color_len = int(math.ceil(math.log(len(self.colors), 2)))
        self.scale_len = int(math.ceil(math.log(params['num_scale'], 2)))

        for i in xrange(popsize):
            tree_genome = createInd.createIndividual(random, params['maxDepth'], params['maxRoom'], params['minRoom'])
            color_genome = [random.randint(0, 1) for i in xrange(color_len)]
            new_ind = DocplanIndividual(random, None, genome={'tree': tree_genome, 'color': color_genome})
            self.initDecode(new_ind)
            pop.append(new_ind)
        
        return pop
    
#-------------------------------------------#
    def initDecode(self, ind):
        '''
        '''
        # decode tree chromosome
        room_list = parseTree.parseTree(ind.genome['tree'], self.params['plotSizeX'], self.params['plotSizeY'])

        tree, shape_list = self.getQuadTree(room_list['sizes'], room_list['desc'])
        ind.genome['tree'] = tree
        ind.shape_list = shape_list

        plan = self.newDecode(tree)

        ind.decoded_plan = plan
        ind.numRoom = plan[0]
        ind.roomarea = plan[1]
        ind.roomlist = plan[2]
        ind.roomDesc = plan[3]
        ind.roomSizes = plan[4]

        # 2nd chromosome
        # decode color chromosome
        chrom = ind.genome['color']
        temp = 0
        len_chrom = len(chrom)
        for i in xrange(len_chrom):
            if chrom[i]:
                temp += 2**(len_chrom-i-1)
        ind.color = temp
    
#-------------------------------------------#
    def decodePlan(self, ind):
        '''
        '''
        # tree decoding
        tree = ind.genome['tree']
        plan = self.newDecode(tree)

        ind.decoded_plan = plan
        ind.numRoom = plan[0]
        ind.roomarea = plan[1]
        ind.roomlist = plan[2]
        ind.roomDesc = plan[3]
        ind.roomSizes = plan[4]
        shape_list = ind.shape_list
        shape_list = self.updateShapeList(tree)
        ind.shape_list = shape_list

        # 2nd chromosome
        # decode color chromosome
        chrom = ind.genome['color']
        temp = 0
        len_chrom = len(chrom)
        for i in xrange(len_chrom):
            if chrom[i]:
                temp += 2**(len_chrom-i-1)
        ind.color = temp


#-------------------------------------------#
    def newDecode(self, tree):
        room_class = []
        room_area = []
        room_sizes = []
        max_val = self.params['max_scale']
        min_val = self.params['min_scale']

        for branch in tree.branch:
            for ind in branch:
                ind.computePos(max_val, min_val)
                room_area.append(ind.getArea())
                room_class.extend([ind.w, ind.l])
                room_sizes.append(list(ind.getPos()))

        room_desc = ['R'] * len(room_area)
        revisedArea = room_area[:]
        revisedArea.sort()

        # call the room-classification routine
        room_desc, num_room = roomClassifier.f1(room_desc, room_sizes,
                                                revisedArea, room_class)

        # call the adjoining-room calculation routine 
        shared_walls = sharedWalls.f1(num_room, room_desc, room_sizes)

        return [num_room, room_area, shared_walls, room_desc, room_sizes]

#-------------------------------------------#
    def getRoomSizes(self, tree):
        room_class = []
        room_areas = []
        room_sizes = []
        for branch in tree.branch:
            for ind in branch:
                room_areas.append(ind.getArea())
                room_class.extend([ind.w, ind.l])
                room_sizes.append(list(ind.getPos()))

        room_desc = ['R'] * len(room_areas)


#-------------------------------------------#
    def updateShapeList(self, tree):
        shape_list = []
        for branch in tree.branch:
            for ind in branch:
                shape_list.append(ind)

        return shape_list

#-------------------------------------------#
    def getQuadTree(self, dimensions, desc):

        max_val = self.params['max_scale']
        min_val = self.params['min_scale']

        coordinates, roomsizes = self.getRoomDesc(dimensions)
        shape_list = self.computeShapeLoc(coordinates, roomsizes, desc, max_val, min_val)

        w, l = self.params['plotSizeX'], self.params['plotSizeY']
        tree = Tree(self.random, w, l)
        for obj in shape_list:
            cx, cy = obj.getCenter()
            if cx < w/2 and cy < l/2:
                tree.branch[0].append(obj)
            elif cx >= w/2 and cy < l/2:
                tree.branch[1].append(obj)
            elif cx < w/2 and cy >= l/2:
                tree.branch[2].append(obj)
            elif cx >= w/2 and cy >= l/2:
                tree.branch[3].append(obj)


        return tree, shape_list

#-------------------------------------------#
    def getRoomDesc(self, dimensions):
        coordinates = []
        roomsizes = []
        xoffset = 0.0
        yoffset = 0.0

        for i in xrange(0, len(dimensions)):
            coordinates.append(float(dimensions[i][0])+xoffset)
            coordinates.append(float(dimensions[i][1])+yoffset)
            roomsizes.append(float(dimensions[i][2])-float(dimensions[i][0]))
            roomsizes.append(float(dimensions[i][3])-float(dimensions[i][1]))

        return coordinates, roomsizes


#-------------------------------------------#
    def computeShapeLoc(self, coordinates, shape_sizes, desc, max_val, min_val):
        '''
        Compute the coordinates and sizes of all shapes.
        '''
        random = self.random
        num_shapes = self.params['num_shapes']
        shape_list = []
        i = 0
        for j in xrange(len(desc)):

            # if not a blank space
            if desc[j] != 'S':

                shape = random.randrange(1, num_shapes+1)
                shape_obj = ShapeObject(random, shape, coordinates[i], coordinates[i+1], 
                        shape_sizes[i], shape_sizes[i+1], self.scale_len)
                shape_obj.computePos(max_val, min_val)
                shape_list.append(shape_obj)

            i += 2

        return shape_list

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

        # begin of shape match
        best.shape_list.sort(lambda a,b: -cmp(a.getArea(), b.getArea()))
        ind.shape_list.sort(lambda a,b: -cmp(a.getArea(), b.getArea()))

        my_shapes = ind.shape_list
        best_shapes = best.shape_list

        best_len = len(best_shapes)
        my_len = len(my_shapes)

        min_len = min(best_len, my_len)
        max_len = max(best_len, my_len)

        match = 0
        for i in xrange(min_len):
            if best_shapes[i].shape_type == my_shapes[i].shape_type:
                match += 1

        subj = match / float(max_len)
        # end of shape match

        self.floorplan_fitness(ind, user_feedback)

        ind.fitness[-1] = 1. - subj


#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panels = []
        for ind in subset:
            ind.shape_list.sort(lambda a,b: -cmp(a.getArea(), b.getArea()))
            doc = docpanel.DocPanel(parentPanel, individual = ind, quad_tree = ind.shape_list, color_scheme=self.colors[ind.color])
            panels.append(doc)

        return panels


#-------------------------------------------#
    def paramSpace(self, pop, user_selected):
        # Using 5 dimensions, 2 obj and 3 subj
        #best = user_selected[0]
        #objmax = [max(best.numRoom-2, 8-best.numRoom)+1., 5., 1.0, 1.0, 1.0]
        #objmin = [0., 0., 0.0, 0.0, 0.0]

        #self.limits = {'max': objmax, 'min': objmin}

        #return objmax, objmin

        # Using 2 dimensions, obj and subj
        best = user_selected[0]
        tmp_objmax = [max(best.numRoom-2, 8-best.numRoom)+1., 5., 1.0, 1.0, 1.0]
        #objmax = [tmp_objmax[2]+tmp_objmax[3], tmp_objmax[0]+tmp_objmax[1]+tmp_objmax[4]]

        objmax = [tmp_objmax[2]+tmp_objmax[3], 1.]
        objmin = [0., 0.]

        self.limits = {'max': objmax, 'min': objmin}

        return objmax, objmin


#-------------------------------------------#
    def report(self, pop, subset, gen):
        '''
        Write to console or file
        population statistics.
        '''
        return
        # minus fitness bias dimension
        #len_fit = len(pop[0].fitness) - 1

        len_fit = len(pop[0].fitness)
        fit = [0.] * len_fit
        top_fit = [0.] * len_fit
        sub_len = len(subset)

        for ind in pop:
            for i in xrange(len_fit):
                fit[i] += (ind.fitness[i] - self.limits['min'][i])/ self.limits['max'][i] * 100.

        for ind in subset:
            for i in xrange(len_fit):
                top_fit[i] += (ind.fitness[i] - self.limits['min'][i])/ self.limits['max'][i] * 100.

        self.best_saved = None

        #pop_len = len(pop)
        #data_str = '%d\t%.5f' % (gen, (fit[2]+fit[3])/float(pop_len))
        #data_str += '\t%.5f' % ((fit[0]+fit[1]+fit[4])/float(pop_len))

        ## print fitness of subset
        #data_str += '\t%.5f' % ((top_fit[2]+top_fit[3])/float(sub_len))
        #data_str += '\t%.5f' % ((top_fit[0]+top_fit[1]+top_fit[4])/float(sub_len))

        #for i in xrange(len_fit):
        #    data_str += '\t%.5f' % (fit[i]/float(pop_len))

        #self.fout.write(data_str + '\n')

#-------------------------------------------#
    def close(self):
        self.fout.close()


#-------------------------------------------#
#-------------------------------------------#
    def floorplan_fitness(self, ind, user_feedback):
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
            penalty +=  (SharedWalls[rels] - SharedBest[rels])**2
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
            fit.extend([1.0, 1.0])
        else:
            penalty = 0.0
            penaltyOne = 0.0
            penaltyTwo = 0.0
            roomDim = []

            if roomNum == 2:
                room_append(Dimensions, roomDim, 'LBK')

                # Minimum dimension of LBK should be 20'10" and minimum area should be 300 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 104.2, 7500.0)

                fit.extend([penaltyOne/104.2, penaltyTwo/7500.0])

            elif roomNum == 3:
                room_append(Dimensions, roomDim, 'LKT')
                room_append(Dimensions, roomDim, 'BED')

                # Minimum dimension of LKT should be 19'10" and minimum area should be 270 sq.ft.
                penaltyOne, penaltyTwo = compute_penalty(roomDim[0], roomDim[1], 99.2, 6750.0)

                # Minimum dimension of BED should be 9'4" and minimum area should be 120 sq.ft.
                pen1_temp, pen2_temp = compute_penalty(roomDim[2], roomDim[3], 46.7, 3000.0)
                penaltyOne += pen1_temp
                penaltyTwo += pen2_temp

                fit.extend([penaltyOne/2.0, penaltyTwo/2.0])

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

                fit.extend([penaltyOne/3.0, penaltyTwo/3.0])

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

                fit.extend([penaltyOne/3.0, penaltyTwo/3.0])
                
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
                
                fit.extend([penaltyOne/4.0, penaltyTwo/4.0])

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

                fit.extend([penaltyOne/5.0, penaltyTwo/5.0])
        
        # 4.Total Built Area
        if roomNum == 0 or roomNum == 1:
            fit.append(1.0)
        else:
            penalty = 0.0
            if sum(totArea) < sum(totAreaBest):
                penalty = (sum(totAreaBest) - sum(totArea))/sum(totAreaBest)

            fit.append(penalty)
            

        #ind.fitness = fit
        obj = fit[2]+fit[3]
        subj = fit[0]+fit[1]+fit[4]
        ind.fitness = [obj, subj]

#-------------------------------------------#
