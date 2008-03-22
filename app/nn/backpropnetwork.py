from node import *
from connection import *
from funcs import dfunc
import random

class BackPropNetwork:
    def __init__(self, input, hidden, output, seed=0):
        self.nodes = {}
        self.id = -1
        self.index = 0
        self.doprop = False
        self.layers = [[], [], []]
        self.inputs = []
        self.outputs = []
        self.tnode = Node("threshold", self.doprop)
        self.tnode.outval = 1.0
        self.oldw = {}

        self.rand = random.Random()
        self.rand.seed(seed)
        for i in xrange(input):
            self.addToInputLayer()
        for i in xrange(hidden):
            self.addToHiddenLayer(self.rand.uniform(-1.0, 1.0))
        for i in xrange(output):
            self.addToOutputLayer(self.rand.uniform(-1.0, 1.0))

    def addToInputLayer(self):
        newnode = self.addNode(0, squash=0)
        conn = Connection(self, newnode, 1.0, self.doprop)
        self.inputs.append(conn)
        newnode.inputs.append(conn)

    def addToOutputLayer(self, threshold):
        newnode = self.addNode(2)
        conn = Connection(newnode, self, 1.0, self.doprop)
        self.outputs.append(conn)
        newnode.outputs.append(conn)

    def addToHiddenLayer(self, threshold):
        newnode = self.addNode(1, threshold)

    def addNode(self, layer, threshold=None, squash=True):
        id = (layer, len(self.layers[layer]))
        newnode = Node(id, self.doprop, squash=squash)
        self.layers[layer].append(newnode)
        if threshold:
            self.addThreshold(newnode, threshold)
        if layer != 0:
            for n in self.layers[layer-1]:
                self.addConnection(n, newnode, self.rand.uniform(-1.0, 1.0))
        if layer != 2:
            for n in self.layers[layer+1]:
                self.addConnection(newnode, n, self.rand.uniform(-1.0, 1.0))
        return newnode

    def addConnection(self, src, dest, weight=1.0):
        conn = Connection(src, dest, weight, self.doprop)
        src.outputs.append(conn)
        dest.inputs.append(conn)

    def addThreshold(self, dest, threshold):
        conn = Connection(self.tnode, dest, threshold)
        self.tnode.outputs.append(conn)
        dest.inputs.append(conn)
        dest.threshold = self.tnode

    def setInput(self, vals):
        if len(vals) != len(self.inputs):
            raise InputSizeError

        for i in xrange(len(vals)):
            self.inputs[i].setValue(float(vals[i]))

        for layer in self.layers:
            for node in layer:
                node.onInput()

    def getOutput(self):
        vals = []
        for o in self.outputs:
            vals.append(o.getValue())
        return vals

    def test(self, pattern):
        right = 0
        wrong = 0
        kap = {}
        for p in pattern:
            input = p[0]
            self.setInput(input)
            output = [int(round(v)) for v in self.getOutput()]
            target = [int(round(v)) for v in p[1]]

            if target == output:
                right += 1
            else:
                wrong += 1
            lt = tuple(p[1])
            rt = tuple(output)
            if not kap.has_key(lt):
                kap[lt] = {}
            if not kap[lt].has_key(rt):
                kap[lt][rt] = 0
            kap[lt][rt] += 1
        return right, wrong, kap

    def adjustWeights(self, input, target, rate, mrate):
        self.setInput(input)
        outnodes = self.layers[2]
        if len(target) != len(outnodes):
            raise ValueError("wrong number of target values")
        deltas = {}
        #output errors
        for k in xrange(len(target)):
            error = target[k] - outnodes[k].outval
            deltas[outnodes[k]] = dfunc(outnodes[k].outval) * error
        
        for node in self.layers[1]:
            error = 0.0
            for conn in node.outputs:
                error += deltas[conn.dest] * conn.weight
            deltas[node] = dfunc(node.outval) * error

        for conn in self.tnode.outputs:
            change = deltas[conn.dest] * conn.weight * rate
            conn.weight += change + self.oldw.get(conn, 0.0) * mrate
            self.oldw[conn] = change
            conn.output = conn.weight

        #find weight changes
        for layer in self.layers:
            for node in layer:
                for conn in node.outputs:
                    if conn.dest.id != -1 and conn.src.id != -1:
                        change = deltas[conn.dest] * conn.input * rate
                        conn.weight += change + self.oldw.get(conn, 0.0) * mrate
                        self.oldw[conn] = change
        
        #find error
        error = 0.0
        for k in xrange(len(target)):
            error += 1.0/len(target) * (target[k] - outnodes[k].outval)**2.0
        return error ** 0.5

    def train(self, patterns, iter, rate, mrate=0.0, fi=None):
        for i in xrange(iter):
            error = 0.0
            for p in patterns:
                input = p[0]
                target = p[1]
                error += self.adjustWeights(input, target, rate, mrate)
            if fi:
                print >> fi, i, error
            else:
                print i, error

class InputSizeError(Exception):
    def __init__(self):
        print "Input size doesn't match number of network inputs"

class OutputSizeError(Exception):
    def __init__(self):
        print "Output size doesn't match number of network outputs"
