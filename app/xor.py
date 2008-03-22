from individual import Individual
from nn import BackPropNetwork
import pickle

class Xor:
    def __init__(self, params, random):
        self.random = random
        inputValue = params['input']
        output = params['output']
        hidden = params['hidden']

        self.nn = BackPropNetwork(inputValue, hidden, output)

        self.ts , self.vs = self.createsets(params)
        self.testing = self.vs
        self.maxerror = float(len(self.ts))

        self.bestFitness = 0.0
        self.totalFitness = 0.0
        self.totalEvals = 0
        self.besttRight = 0
        self.bestvRight = 0


#---------------------------------------#
    def createPop(self, popsize):
        print "Creating Population...",
        #sys.stdout.flush()
        pop = []
        for layer in self.nn.layers[1:]:
            for node in layer:
                subpop = []
                for i in xrange(popsize):
                    genome = []
                    for conn in node.inputs:
                        genome.append(self.random.uniform(-1.0, 1.0))
                    subpop.append(Individual(None, None, genome))
                pop.append(subpop)
        print "Done"
        return pop


#---------------------------------------#
    def fitness(self, indset):
        #self.nn.clear()
        #print "\t["+len(self.ts)/1000*' '+"]\r\t[",
        #sys.stdout.flush()
        self.initnet(indset)
        
        error = 0.0
        tright = 0
        for p in self.ts:
            inputValue = p[0]
            target = p[1]
            self.nn.setInput(inputValue)
            output = self.nn.getOutput()
            N = len(target)
            e = 0.0
            for k in xrange(len(target)):
                e += (1.0/N) * (target[k] - output[k]) ** 2
            #params['seed']e = e ** 0.5
            error += e
        
        fitness = self.maxerror - error# + tright
        if fitness > self.bestFitness:
            self.bestFitness = fitness
        self.totalFitness += fitness
        self.totalEvals += 1
        for ind in indset:
            ind.fitness += fitness


#---------------------------------------#
    def scaleFitness(self, pop):
        for subpop in pop:
            minfit = self.maxerror
            maxfit = 0
            sumfit = 0
            N = len(subpop)
            mult = 1.2
            for i in subpop:
                if i.fitness < minfit:
                    minfit = i.fitness
                if i.fitness > maxfit:
                    maxfit = i.fitness
                sumfit += i.fitness
            avgfit = sumfit / N

            if minfit > (mult * avgfit - maxfit) / (mult - 1.0):
                delta = maxfit - avgfit
                a = (mult - 1.0) * avgfit / delta
                b = avgfit * (maxfit - mult*avgfit) / delta
            else:
                delta = avgfit -  minfit
                a = avgfit / delta
                b = -minfit * avgfit / delta

            for i in subpop:
                i.scalefit = i.fitness * a + b


#---------------------------------------#
    def report(self, pop, gen):

        indset = []
        for subpop in pop:
            maxfit = 0
            for ind in subpop:
                if ind.fitness > maxfit:
                    maxfit = ind.fitness
                    best = ind
            indset.append(best)

        self.initnet(indset)

        right = 0
        tset = self.testing
        #sys.stdout.flush()
        print ''
        for i in tset:
            self.nn.setInput(i[0])
            output = self.nn.getOutput()

            print 'input: ', i[0], 'output:', output

        vRight = right

        if vRight > self.bestvRight:
            self.bestvRight = vRight
            self.bestnn = pickle.dumps(self.nn)

        #print "\r", " " * 60,
        #print '\r%i) best fit: %.2f, avg fit: %.2f, training/validation right: %.2f / %.2f' % \
        #            (gen, self.bestFitness, self.totalFitness/self.totalEvals, self.besttRight/self.maxerror*100, self.bestvRight/self.maxerror*100)

        self.bestFitness = self.besttRight = self.totalFitness = self.totalEvals = 0.0
        print ''


#---------------------------------------#
    def initnet(self, indset):
        '''
        Decode network weights and load them to NN.
        '''
        indnum = 0
        for layer in self.nn.layers[1:]:
            for node in layer:
                ind = indset[indnum]
                for i in xrange(len(node.inputs)):
                    node.inputs[i].weight = ind.genome[i]
                indnum += 1


#---------------------------------------#
    def createsets(self, params):
        import random
        #self.rand = random.Random(params['seed'])
        self.rand = random.Random()

        # two bit xor
        #trainingset = [ [[0, 0],[0]],
        #                [[0, 1],[1]],
        #                [[1, 0],[1]],
        #                [[1, 1],[0]] ]

        #testingset = [ [[0, 0],[0]],
        #                [[0, 1],[1]],
        #                [[1, 0],[1]],
        #                [[1, 1],[0]] ]

        trainingset = [ [[0, 0, 0], [0]],
                        [[0, 1, 0], [1]],
                        [[1, 0, 0], [1]],
                        [[1, 1, 0], [0]],
                        [[0, 0, 1], [1]],
                        [[0, 1, 1], [0]],
                        [[1, 0, 1], [0]],
                        [[1, 1, 1], [1]] ]

        testingset =  [ [[0, 0, 0], [0]],
                        [[0, 1, 0], [1]],
                        [[1, 0, 0], [1]],
                        [[1, 1, 0], [0]],
                        [[0, 0, 1], [1]],
                        [[0, 1, 1], [0]],
                        [[1, 0, 1], [0]],
                        [[1, 1, 1], [1]] ]


        return trainingset, testingset


