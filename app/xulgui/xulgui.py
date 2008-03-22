from iga.individual import Individual
from iga.gacommon import gaParams
import string
import app.app as app

from app.helperfuncs import hamming,lcs

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

        # used to compute the number of fonts in machine
        # can't use it when working accross machines
        #if self.attr.has_key('font_face'):
        #    import wx, math
        #    faces = wx.FontEnumerator.GetFacenames()
        #    max = len(faces) - 1
        #    varBits = int(math.ceil(math.log(max, 2)))
        #    self.attr['font_face']['bits'] = varBits
        #    self.attr['font_face']['max'] = max
        #    self.attr['font_face']['min'] = 0
        #    self.geneLen += varBits


        #folder, outputFile = params['folder'], params['output']
        #fout = open(folder + outputFile, 'w')
        #fout.write('gen \t max \t avg \t min \t opt \t obj_max \t obj_avg \t obj_min \t subj_max \t subj_avg \t subj_min\n')
        #self.fout = fout

        import time
        ltime = time.localtime()
        hour, min = ltime[3], ltime[4]
        self.fout = open('data/%s_pop_%d-%d' % (params['name'], hour, min), 'w')
        self.fout.write('gen\tobj\tsubj\tdiversity\n')

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
        idList = []

        uiWidgets = {}
        # ID list is location in XML tree + 1 in order to prevent having a zero ID value
        for i in xrange(len(ui_data.childNodes)):
            if ui_data.childNodes[i].nodeType == self.ELEMENT_NODE:
                widgetNum += 1

                # Store in list representation to be used to generate wxPython code
                data = {}
                nodeName = ui_data.childNodes[i].nodeName
                data['name'] = nodeName
                data['value'] = ui_data.childNodes[i].getAttribute('value')
                data['size'] = ui_data.childNodes[i].getAttribute('size')
                data['bind'] = ui_data.childNodes[i].getAttribute('bind')
                data['id'] = ui_data.childNodes[i].getAttribute('id')
                data['id'] = eval(data['id'])
                idList.append(data['id'])
                if data['bind']:
                    data['bind'] = eval(data['bind'])
                if data['size']:
                    data['size'] = eval(data['size'])
                uiWidgets[idList[-1]] = data

        self.uiWidgets = uiWidgets
        self.maxDist = ( (255*255) * 3. )**0.5

        # objective component bounds
        self.objMax = 200

        # Create chromosome of widget ids
        gridChrom = [0] * self.gridSize
        gridChrom[:len(idList)] = idList[:]
        self.gridLen = len(gridChrom)

        # subjective component bounds
        # widgets + window
        self.subjMax = self.gridLen + self.geneLen

        self.widgetNum = widgetNum

        pop = []
        for i in xrange(popsize):
            self.random.shuffle(gridChrom)
            pop.append(XulIndividual(None, None, {'grid':gridChrom[:], 'style':[self.random.randint(0, 1) for i in xrange(self.geneLen)]}))

        return pop


#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        user_feedback is [best]
        '''
        best = user_feedback[0]
        widgetNum = self.widgetNum
        subj = 0
        subj += lcs(ind.genome['grid'], best.genome['grid'])
        subj += lcs(ind.genome['style'], best.genome['style'])


        #-------------------------------------------------------------#
        # BEGIN OBJECTIVE EVALUATION
        #-------------------------------------------------------------#
        grid, myValues = self.decode(ind)
        red = green = blue = 0
        # and the background color
        # A high value is good
        # window color is stored at pos 0
        red = myValues['window_red'] - myValues['widget_red']
        green = myValues['window_green'] - myValues['widget_green']
        blue = myValues['window_blue'] - myValues['widget_blue']

        distance = (red*red + green*green + blue*blue)**0.5
        obj = distance / self.maxDist * 100.

        grid_max = self.gridLen - 1.
        ui = self.uiWidgets
        layout_score = 0.
        num_binds = 0
        for id in grid:
            if id:
                if ui[id]['bind']:
                    other = grid.index(ui[id]['bind'])
                    me = grid.index(id)
                    diff = abs(other - me)
                    if diff < 3:
                        layout_score += 1.
                    else:
                        layout_score += (grid_max-diff)/grid_max

                    num_binds += 1.

        if num_binds:
            val = layout_score/num_binds * 100.
            obj += val
        else:
            obj += 100.

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
    def report(self, pop, subset, gen):
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

        # minus fitness bias dimension
        #len_fit = len(pop[0].fitness) - 1
        #fit = [0.] * len_fit

        #for ind in pop:
        #    for i in xrange(len_fit):
        #        fit[i] += (ind.fitness[i] - self.limits['min'][i])/ self.limits['max'][i]

        #pop_len = len(pop)
        #self.fout.write('%d\t%.5f\t%.5f\n' % (gen, fit[0]/pop_len, fit[1]/pop_len))


        avg_hd = 0.
        pop_len = len(pop)
        for i in xrange(pop_len-1):
            for j in xrange(i+1, pop_len):
                avg_hd += hamming(pop[i].genome['grid']+pop[i].genome['style'],
                        pop[j].genome['grid']+pop[j].genome['style'])

        avg_hd /= float(pop_len)
        self.fout.write('%d\t%.5f\n' % (gen, avg_hd))

        f = open('data/xul_gen_%d' % gen, 'w')
        i = 0
        pop.sort(lambda a,b: cmp(a.rank, b.rank))
        for i in xrange(10):
            f.write('%.2f %.2f\n' % (pop[i].fitness[0], pop[i].fitness[1]))
        f.close()


#-------------------------------------------#
    def test(self, pop):
        # then do clean up stuff
        self.close()


#-------------------------------------------#
    def close(self):
        self.fout.close()

##------------------------------------------#
#    def decodeColor(self, chrom):
#        '''
#        Decodes the chromosome from binary to decimals or floats, or whatever it may be.
#        '''
#        step = self.bits / 3
#        values = []
#        for i in xrange(0, self.geneLen, self.bits):
#            color = []
#            color.append(int(string.joinfields(map(str, chrom[i:i+step]), ''), 2))
#            color.append(int(string.joinfields(map(str, chrom[i+step:i+step*2]), ''), 2))
#            color.append(int(string.joinfields(map(str, chrom[i+step*2:i+step*3]), ''), 2))
#
#            values.append(color)
#
#        return values

#------------------------------------------#
    def decode(self, ind):
        '''
        Decodes the chromosome from binary to decimals or floats, or whatever it may be.
        '''
        grid = ind.genome['grid']
        style = self.decodeStyle(ind.genome['style'])

        return grid, style

#-------------------------------------------#
    def decodeStyle(self, chrom):
        '''
        Decode bit string.
        '''
        bits = 0
        data = {}
        for name,value in self.attr.iteritems():
            temp = 0
            top = int(bits+value['bits'])
            for i in xrange(int(bits), top):
                if chrom[i]:
                    temp += 2**(top-i-1)

            temp = temp / (2.**value['bits'] - 1)
            temp =  temp * (value['max']-value['min']) + value['min']
            data[name] = temp
            bits += value['bits']

        return data

#-------------------------------------------#
    def paramSpace(self, pop, user_selected):
        objmax = [self.objMax, self.subjMax]
        objmin = [self.objMin, self.subjMin]
        self.limits = {'max': objmax, 'min': objmin}
        return objmax, objmin

#-------------------------------------------#
    def close(self):
        self.fout.close()

#------------------------------------------#
