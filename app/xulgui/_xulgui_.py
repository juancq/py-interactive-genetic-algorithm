from iga.individual import Individual
from iga.gacommon import gaParams
import random, string
import app.app as app

from app.helperfuncs import hamming, lcs

#-------------------------------------------#
class XulIndividual(Individual):
    def __init__(self, random, genome_len, genome):
        Individual.__init__(self, random, genome_len, genome)
        self.rank = 0

    def __cmp__(self, other):
        return cmp(self.rank, other.rank)

#-------------------------------------------#
class Xulgui(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)
        self.geneLen = 0.
        self.bits = params['bits']


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
        # contains actual location of widgets in XML tree
        elementNodes = []
        # ID list is location in XML tree + 1 in order to prevent having a zero ID value
        idList = []
        for i in xrange(len(ui_data.childNodes)):
            if ui_data.childNodes[i].nodeType == self.ELEMENT_NODE:
                elementNodes.append(i)
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

        self.geneLen = widgetNum * self.bits + self.bits
        # this is wrong, this is for HSV
        self.maxDist = ( (360*360) + (100*100) + (100*100) )**0.5

        import operator
        def factorial(x): return reduce(operator.mul, xrange(2, x + 1))

        # count the number of combinations of 2 widgets available
        # this counts comparisons between widgets
        comps = factorial(widgetNum - 1) / (factorial(widgetNum-1 - 2) * 2)
        # this counts comparisons between each widget to window
        comps += widgetNum - 1

        # objective component bounds
        # each comparison is worth a max of 100
        self.objMax = comps * 100

        # Create chromosome of widget ids
        gridChrom = [0] * self.gridSize
        gridChrom[:len(idList)] = idList[:]
        self.gridLen = len(gridChrom)

        # subjective component bounds
        # widgets + window
        #self.subjMax = ((widgetNum + 1) * 100.) + (100. * self.gridLen)
        self.subjMax = self.gridLen + self.geneLen

        # if comparing to best and worst, then increase subjective max scale accordingly
        if self.params['compare'] == 'both':
            self.subjMax *= 2

        self.widgetNum = widgetNum
        self.elementNodes = elementNodes

        pop = []
        for i in xrange(popsize):
            random.shuffle(gridChrom)
            pop.append(XulIndividual(None, None, {'grid':gridChrom[:], 'style':[random.randint(0, 1) for i in xrange(self.geneLen)]}))

        return pop


#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is [best,worst]
        '''
        best,worst = user_feedback
        subj = 0
        widgetNum = self.widgetNum
        if ind.genome == best.genome:
            subj = 2 * len(ind.genome['grid'])+len(ind.genome['style'])
        elif ind.genome == worst.genome:
            subj = 0
        else:
            #sum += lcs(ind.genome, best.genome)
            #sum += len(ind.genome)-lcs(ind.genome, worst.genome)
            subj += hamming(ind, best, worst)


        #-------------------------------------------------------------#
        # BEGIN OBJECTIVE EVALUATION
        #-------------------------------------------------------------#
        red = green = blue = 0
        colorFitness = 0
        myValues = self.decode(ind.genome['style'])
        # Compare widget colors, we want the colors to be similar, so a low value is good
        # start from 1, since at pos 0 we store window color
        for i in xrange(1, widgetNum - 1):
            for j in xrange(i + 1, widgetNum):
                red = abs(myValues[i][0] - myValues[j][0])
                green = abs(myValues[i][1] - myValues[j][1])
                blue = abs(myValues[i][2] - myValues[j][2])

                distance = (red*red + green*green + blue*blue)**0.5

                colorFitness += (self.maxDist-distance) / self.maxDist * 100.

        windColor = 0
        # compare all widgets to the window color, we want a high color diff between each widget
        # and the background color
        # A high value is good
        for i in xrange(1, widgetNum):
            # window color is stored at pos 0
            red = abs(myValues[i][0] - myValues[0][0])
            green = abs(myValues[i][1] - myValues[0][1])
            blue = abs(myValues[i][2] - myValues[0][2])

            distance = (red*red + green*green + blue*blue)**0.5
            windColor += distance / self.maxDist * 100.


        obj = colorFitness + windColor
        #-------------------------------------------------------------#
        # END OBJECTIVE EVALUATION
        #-------------------------------------------------------------#
        subj = float(subj)
        # Scale objective and subjective fitness components
        objFitness = (obj-self.objMin)/(self.objMax-self.objMin) * self.objScaleMax + self.objScaleMin
        subjFitness = (subj-self.subjMin)/(self.subjMax-self.subjMin) * self.subjScaleMax + self.subjScaleMin

        w1, w2 = self.params['weight1'], self.params['weight2']
        #ind.scalefit = ind.fitness = objFitness * w1 + subjFitness * w2
        ind.objFitness = objFitness
        ind.subjFitness = subjFitness
        ind.fitness = [objFitness, subjFitness]


#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panels = []
        import evolveuipanel as individual_panel
        for i in xrange(len(subset)):
            grid = subset[i].genome['grid']
            style = self.decode(subset[i].genome['style'])
            panels.append(individual_panel.IndividualPanel(parentPanel, i, style, grid, self.uiWidgets))

        return panels

#-------------------------------------------#
    def report(self, pop, gen):
        app.Application.report(self, pop, gen)
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
        print 'Test'

        # then do clean up stuff
        self.close()


#-------------------------------------------#
    def close(self):
        self.fout.close()

#------------------------------------------#
    def decode(self, chromosome):
        '''
        Decodes the chromosome from binary to decimals or floats, or whatever it may be.
        '''
        # RGB DECODING
        values = []
        step = self.bits / 3
        for i in xrange(0, self.geneLen, self.bits):
            color = []
            color.append(int(string.joinfields(map(str, chromosome[i:i+step]), ''), 2))
            color.append(int(string.joinfields(map(str, chromosome[i+step:i+step*2]), ''), 2))
            color.append(int(string.joinfields(map(str, chromosome[i+step*2:i+step*3]), ''), 2))

            values.append(color)

        return values

#-------------------------------------------#
    def paramSpace(self, pop, user_selected):
        objmax = [self.objMax, self.subjMax]
        objmin = [self.objMin, self.subjMin]
        return objmax, objmin

#------------------------------------------#
#-------------------------------------------#
