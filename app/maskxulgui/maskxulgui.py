from iga.individual import Individual
from iga.gacommon import gaParams
import string
import app.maskapp as maskapp

from app.helperfuncs import ham

#-------------------------------------------#
class XulIndividual(Individual):
    def __init__(self, random, genome_len, genome):
        Individual.__init__(self, random, genome_len, genome)
        self.rank = 0

    def __cmp__(self, other):
        return cmp(self.rank, other.rank)

#-------------------------------------------#
class Maskxulgui(maskapp.MaskApplication):
    def __init__(self, params, random):
        maskapp.MaskApplication.__init__(self, params, random)

        self.bits = self.params['bits']

        folder, outputFile = params['folder'], params['output']
        fout = open(folder + outputFile, 'w')
        fout.write('gen \t max \t avg \t min \t opt \t obj_max \t obj_avg \t obj_min \t subj_max \t subj_avg \t subj_min\n')
        self.fout = fout

        self.uiWidgets = None
        self.maxDist = 0.
        self.objMax = 0.
        self.objMin = 0.
        self.objScaleMax = params['objScaleMax']
        self.objScaleMin = params['objScaleMin']
        self.gridSize = params['rows'] * params['cols']
        self.subjMax = 0.
        self.subjMin = 0.
        self.subjScaleMax = params['subjScaleMax']
        self.subjScaleMin = params['subjScaleMin']


#-------------------------------------------#
    def createPop(self, popsize):

        #Parse user interface.
        #Compute how many widgets there are in the UI.
        import xml.dom.minidom
        dom = xml.dom.minidom.parse('app/xulgui/'+self.params['ui_file'])
        panel = dom.getElementsByTagName('panel')
        ui_data = panel[0].cloneNode(True)
        dom.unlink()

        self.ELEMENT_NODE = xml.dom.minidom.Node.ELEMENT_NODE
        widgetNum = 0

        uiWidgets = {}
        # ID list is location in XML tree + 1 in order to prevent having a zero ID value
        idList = []
        for i in xrange(len(ui_data.childNodes)):
            if ui_data.childNodes[i].nodeType == self.ELEMENT_NODE:
                idList.append(i + 1)
                widgetNum += 1

                # Store in list representation to be used to generate wxPython code
                data = {}
                nodeName = ui_data.childNodes[i].nodeName
                data['name'] = nodeName
                data['value'] = ui_data.childNodes[i].getAttribute('value')
                data['size'] = ui_data.childNodes[i].getAttribute('size')
                if data['size']:
                    data['size'] = eval(data['size'])
                uiWidgets[i+1] = data

        self.uiWidgets = uiWidgets

        self.geneLen = self.bits + self.bits
        self.maxDist = ( (255*255) * 3. )**0.5

        # objective component bounds
        self.objMax = 100

        # Create chromosome of widget ids
        gridChrom = [0] * self.gridSize
        gridChrom[:len(idList)] = idList[:]
        self.gridLen = len(gridChrom)

        # subjective component bounds
        # widgets + window
        self.subjMax = self.gridLen + self.geneLen

        self.widgetNum = widgetNum

        defaults = {}
        defaults['style'] = [[0, 0, 0], [255, 255, 255]]
        defaults['grid'] = gridChrom[:]
        pop = []
        for i in xrange(popsize):
            chrom = {}
            if self.attr['style']['mask']:
                chrom['style'] = None
            else:
                chrom['style'] = [self.random.randint(0, 1) for i in xrange(self.geneLen)]
            if self.attr['grid']['mask']:
                chrom['grid'] = None
            else:
                self.random.shuffle(gridChrom)
                chrom['grid'] = gridChrom[:]

            ind = XulIndividual(None, None, chrom)
            ind.defaults = defaults.copy()
            pop.append(ind)

        return pop


#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is [best,worst]
        '''
        best = user_feedback[0]
        subj = 0
        widgetNum = self.widgetNum
        for attr_name, chrom in ind.genome.iteritems():
            if chrom:
                subj += ham(best.genome[attr_name], chrom)


        #-------------------------------------------------------------#
        # BEGIN OBJECTIVE EVALUATION
        #-------------------------------------------------------------#
        grid, myValues = self.decode(ind)
        red = green = blue = 0
        # and the background color
        # A high value is good
        # window color is stored at pos 0
        red = myValues[1][0] - myValues[0][0]
        green = myValues[1][1] - myValues[0][1]
        blue = myValues[1][2] - myValues[0][2]

        distance = (red*red + green*green + blue*blue)**0.5
        obj = distance / self.maxDist * 100.

        #-------------------------------------------------------------#
        # END OBJECTIVE EVALUATION
        #-------------------------------------------------------------#
        subj = float(subj)
        # Scale objective and subjective fitness components
        objFitness = (obj-self.objMin)/(self.objMax-self.objMin) * self.objScaleMax + self.objScaleMin
        subjFitness = (subj-self.subjMin)/(self.subjMax-self.subjMin) * self.subjScaleMax + self.subjScaleMin

        ind.objFitness = objFitness
        ind.subjFitness = subjFitness
        ind.fitness = [self.objScaleMax-objFitness, self.subjScaleMax-subjFitness]

        # pareto thing is minimizing!!!


#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panels = []
        import evolveuipanel as individual_panel
        for i in xrange(len(subset)):
            grid, style = self.decode(subset[i])
            panels.append(individual_panel.IndividualPanel(parentPanel, i, style, grid, self.uiWidgets))

        return panels

#-------------------------------------------#
    def report(self, pop, gen):
        maskapp.MaskApplication.report(self, pop, gen)
        maxFit = 0.0
        sumFit = 0.0
        minFit = 100000.0

        sumObjFit = 0.0
        sumSubjFit = 0.0
        
        best = None
        worst = None

        ## this can be replaced with a max and min function
        #for ind in pop:
        #    if ind.fitness > maxFit:
        #        maxFit = ind.fitness
        #        best = ind

        #    if ind.fitness < minFit:
        #        minFit = ind.fitness
        #        worst = ind
        #                
        #    sumFit += ind.fitness
        #    sumObjFit += ind.objFitness
        #    sumSubjFit += ind.subjFitness
        #    
        #popLen = len(pop)
        #print '%i) Best Fit: %.2f, Avg Fit: %.2f' % (gen, best.fitness, sumFit/popLen)


        ## Compute avg objective and subjective fitness
        #objFit = sumObjFit / popLen
        #subjFit = sumSubjFit / popLen

        ## gen max avg min opt
        #self.fout.write("%5d %10.2f %10.2f %10.2f " % (gen, 
        #            best.fitness, sumFit/len(pop), worst.fitness))

        ## obj_max obj_avg obj_min subj_max subj_avg subj_min
        #self.fout.write("%10.2f %10.2f %10.2f %10.2f %10.2f %10.2f\n" % (best.objFitness, objFit, 
        #            worst.objFitness, best.subjFitness, subjFit, worst.subjFitness))



#-------------------------------------------#
    def test(self, pop):
        # then do clean up stuff
        self.close()


#-------------------------------------------#
    def close(self):
        self.fout.close()

#------------------------------------------#
    def decodeColor(self, chrom):
        '''
        Decodes the chromosome from binary to decimals or floats, or whatever it may be.
        '''
        step = self.bits / 3
        values = []
        for i in xrange(0, self.geneLen, self.bits):
            color = []
            color.append(int(string.joinfields(map(str, chrom[i:i+step]), ''), 2))
            color.append(int(string.joinfields(map(str, chrom[i+step:i+step*2]), ''), 2))
            color.append(int(string.joinfields(map(str, chrom[i+step*2:i+step*3]), ''), 2))

            values.append(color)

        return values

#------------------------------------------#
    def decode(self, ind):
        '''
        Decodes the chromosome from binary to decimals or floats, or whatever it may be.
        '''
        grid = None
        if ind.genome['grid']:
            grid = ind.genome['grid']
        else:
            grid = ind.defaults['grid']

        style = None
        if ind.genome['style']:
            style = self.decodeColor(ind.genome['style'])
        else:
            style = ind.defaults['style']

        return grid, style


#-------------------------------------------#
    def updateMask(self, pop, mask):
        '''
        Update chromosome of each individual with new mask.
        If value is being masked, then decode current value
        '''
        attr = self.attr
        randint = self.random.randint
        shuffle = self.random.shuffle

        for var in mask:
            attr[var]['mask'] = not attr[var]['mask']
            if var == 'style':
            # i.e. expanding search space
            # if not initialized before, then # create random chrom for attribute
                if not attr[var]['mask']:
                    for ind in pop:
                        ind.genome[var] = [randint(0, 1) for i in xrange(self.geneLen)]
            elif var == 'grid':
            # i.e. expanding search space
            # if not initialized before, then # create random chrom for attribute
                if not attr[var]['mask']:
                    for ind in pop:
                        shuffle(ind.defaults[var])
                        ind.genome[var] = ind.defaults[var][:]

#-------------------------------------------#
    def paramSpace(self, pop, user_selected):
        objmax = [self.objMax, self.subjMax]
        objmin = [self.objMin, self.subjMin]
        return objmax, objmin

#------------------------------------------#
