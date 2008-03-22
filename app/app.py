import wx
from iga.individual import Individual
from pickle import dumps
import math

#-------------------------------------------#
class Application:
    def __init__(self, params, random):
        self.random = random
	self.params = params

        # if user provided list of variables to encode
       # then determine the number of bits
       # necessary to encode the variables
        if self.params.has_key('vars'):
            var_list = self.params['vars']
            bits = 0
            attr = {}
            for name,value in var_list.iteritems():
                attr[name] = value.copy()
                if value.has_key('scale'):
                    scale = value['scale']
                else:
                    scale = 1
                if value.has_key('max') and value.has_key('min'):
                    varBits = int(math.ceil(math.log((value['max']-value['min'])/float(scale), 2)))
                    bits += varBits
                    attr[name]['bits'] = varBits

            self.attr = attr
            self.geneLen = bits
        else:
            self.geneLen = self.params['bits']
            self.attr = None



        #import time
        #ltime = time.localtime()
        #hour, min = ltime[3], ltime[4]
        #self.fb = open('data/%s_blood_%d-%d' % (params['name'], 
        #            hour, min), 'w')
        #self.fb.write('gen  full  3quarter half quarter mud\n')

        #self.fpop = open('data/%s_pop_%d-%d' % (params['name'], 
        #            hour, min), 'w')
        #self.fpop.write('gen  pop\n')

        #self.ffit = open('data/%s_fit_%d-%d' % (params['name'], hour, min), 'w')
        #self.ffit.write('gen  sum_fitness\n')

#-------------------------------------------#
    def createPop(self, popsize):        
        pop = [Individual(self.random, self.geneLen) for i in xrange(popsize)]
        return pop

#-------------------------------------------#
    def decode(self, ind):
        '''
        Decode bit string.
        '''
        chrom = ind.genome
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

        ind.decoded_chrom = data.copy()

        return data
        
#-------------------------------------------#
    def fitness(self, ind, user_feedback):
        '''
        Compute fitness.
        '''
        ind.fitness = sum(ind.genome)

#-------------------------------------------#
    def scaleFitness(self, pop):
        for ind in pop:
            ind.scalefit = ind.fitness

#-------------------------------------------#
    def draw(self, parentPanel, subset):
        '''
        Return a list of panels to be displayed to the user for evaluation.
        Use the arg parentPanel as the parent for each of the panels created.
        '''
        panel = []
        for i in xrange(len(subset)):
            panel.append(wx.Panel(parentPanel))
        return panel

#-------------------------------------------#
    def report(self, pop, gen):
        '''
        Write to console or file
        population statistics.
        '''
        pass
        #fb = self.fb
        blood = {'full': 0, 'half': 0, 
                'quarter': 0, 'mud': 0, 
                '3quarter':0, }

        for ind in pop:
            if ind.bloodline == 0.:
                blood['mud'] += 1

            elif ind.bloodline == 1.:
                blood['full'] += 1

            elif ind.bloodline == 0.5:
                blood['half'] += 1

            elif ind.bloodline < 0.5:
                blood['quarter'] += 1

            else:
                blood['3quarter'] += 1

                        
        blood_str = '%d  %d  %d  %d  %d  %d\n' % (gen, blood['full'],
                        blood['3quarter'], blood['half'], 
                        blood['quarter'], blood['mud'])
        #fb.write(blood_str)

        # dump pop pickle
        #self.fpop.write('%d %s\n' % (gen, dumps(pop)))

#-------------------------------------------#
    def test(self, pop):
        pass
        #self.fb.close()
        #self.fpop.close()

#-------------------------------------------#
    def preFitnessEval(self, pop, gen):
        pass

#-------------------------------------------#
    def postFitnessEval(self, pop, gen):
        pass

#-------------------------------------------#
    def close(self):
        pass

#-------------------------------------------#
    def paramSpace(self, pop, user_selected):
        return [],[]

#-------------------------------------------#
