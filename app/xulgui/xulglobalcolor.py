from individual import Individual
from gacommon import gaParams
import random, string
from helperfuncs import hamming, lcs


#-------------------------------------------#
class Xulglobalcolor:
    def __init__(self, params, random):
        self.random = random
        self.geneLen = 0
        self.bits = params['bits']
        self.params = params

        self.gridSize = params['rows'] * params['cols']

        self.objScaleMax = params['objScaleMax']
        self.objScaleMin = params['objScaleMin']
        self.subjMax = 0.
        self.subjMin = 0.
        self.subjScaleMax = params['subjScaleMax']
        self.subjScaleMin = params['subjScaleMin']

    def createPop(self, popsize):

        #Parse user interface.
        #Compute how many widgets there are in the UI.
        import xml.dom.minidom
        dom = xml.dom.minidom.parse(self.params['ui_file'])
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
                uiWidgets[i+1]= data

        self.uiWidgets = uiWidgets

        self.geneLen = self.bits + self.bits
        
        # wrong, need to change to RGB
        self.maxDist = ( (360*360) + (100*100) + (100*100) )**0.5

        # objective component bounds
        self.objMax = 100
        self.objMin = 0

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
            pop.append(Individual(None, None, {'grid':gridChrom[:], 'style':[random.randint(0,1) for i in xrange(self.geneLen)]}))

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
        myValues = self.decode(ind.genome['style'])
        # compare global widget color to background window color
        # window color is stored at pos 0
        red = abs(myValues[1][0] - myValues[0][0])
        green = abs(myValues[1][1] - myValues[0][1])
        blue = abs(myValues[1][2] - myValues[0][2])

        distance = (red*red + green*green + blue*blue)**0.5
        windColor = distance / self.maxDist * 100.

        obj = windColor
        #-------------------------------------------------------------#
        # END OBJECTIVE EVALUATION
        #-------------------------------------------------------------#
        subj = float(subj)
        # Scale objective and subjective fitness components
        objFitness = (obj-self.objMin)/(self.objMax-self.objMin) * self.objScaleMax + self.objScaleMin
        subjFitness = (subj-self.subjMin)/(self.subjMax-self.subjMin) * self.subjScaleMax + self.subjScaleMin

        w1, w2 = self.params['weight1'], self.params['weight2']
        ind.scalefit = ind.fitness = objFitness * w1 + subjFitness * w2

#-------------------------------------------#
    def scaleFitness(self, pop):
        pass

#-------------------------------------------#
    def draw(self, parentPanel, subset, population):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panels = []
        import panel.globalcolor_panel as individual_panel
        for i in xrange(len(subset)):
            grid = subset[i].genome['grid']
            style = self.decode(subset[i].genome['style'])
            panels.append(individual_panel.IndividualPanel(parentPanel, i, style, grid, self.uiWidgets))

        return panels


#-------------------------------------------#
    def report(self, pop, gen):
        maxFit = 0.0
        sumFit = 0.0
        for ind in pop:
            if ind.fitness > maxFit:
                maxFit = ind.fitness
                best = ind
            sumFit += ind.fitness
            
        print '%i) Best Fit: %.2f, Avg Fit: %.2f' % (gen, best.fitness, sumFit/len(pop))


#-------------------------------------------#
    def test(self, pop):
        print 'Test'

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

#------------------------------------------#
#-------------------------------------------#
