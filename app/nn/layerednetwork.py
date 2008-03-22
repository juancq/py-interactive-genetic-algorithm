from network import *

class LayeredNetwork(Network):
    def __init__(self, hiddenLayers=0):
        Network.__init__(self)
        self.doprop = False
        self.layers = []
        for i in xrange(2+hiddenLayers):
            self.layers.append(0)

    def setInput(self, vals):
        if len(vals) != len(self.outputs):
            raise InputSizeError
        #for conn in self.outputs:
        #    conn.clear()
        for i in xrange(len(vals)):
            self.outputs[i].setValue(float(vals[i]))

        #for tnode in self.tnodes.values():
        #    tnode.outputs[0].setValue(1.0)
        for i in xrange(len(self.layers)):
            for j in xrange(self.layers[i]):
                node = self.nodes[(i,j)]
                node.onInput()

        #self.outputs[len(vals)].setValue(1.0)

    def addNode(self, threshold, layer):
        if layer > len(self.layers):
            raise AddError(layer)
        if layer == -1:
            layer = len(self.layers)-1
        elif layer < -1:
            raise AddError(layer)
        id = (layer, self.layers[layer])
        self.layers[layer] += 1
        Network.addNode(self, id, threshold)
        node = self.nodes[id]
        if layer != 0:
            for i in xrange(self.layers[layer-1]):
                self.addConnection((layer-1, i), id)
        if layer != len(self.layers)-1:
            for j in xrange(self.layers[layer+1]):
                self.addConnection(id, (layer+1, j))
        return id

    def addToInputLayer(self):
        i = self.addNode(None, 0)
        self.addInput(i)

    def addToOutputLayer(self, threshold):
        o = self.addNode(threshold, -1)
        self.addOutput(o)

    def getOutputNodes(self):
        outlayer = len(self.layers)-1
        layer = []
        for i in xrange(self.layers[outlayer]):
            layer.append(self.nodes[(outlayer, i)])
        return layer

class AddError(Exception):
    def __init__(self, value):
        self.value = value
        print "Undefined Layer: ", value
    def __str__(self):
        return repr(self.value)
