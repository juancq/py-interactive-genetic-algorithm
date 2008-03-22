from node import Node
from connection import Connection

class Network(Node):
    def __init__(self):
        Node.__init__(self, -1)
        self.nodes = {}
        self.connections = {}
        self.index = 0
        self.tnodes = {}
        self.doprop = True

    def addNode(self, id=None, threshold=1.0):
        if not id:
            id = self.index
        if self.nodes.has_key(id):
            print self.nodes.keys()
            raise NodeDefinedError(id)
        self.nodes[id] = Node(id, self.doprop)
        if threshold:
            self.addThreshold(id, threshold)
        return id

    def setInput(self, vals):
        if len(vals) != len(self.outputs):
            raise InputSizeError
        for conn in self.outputs:
            conn.clear()
        for i in xrange(len(vals)):
            self.outputs[i].setValue(float(vals[i]))
        #self.outputs[len(vals)].setValue(1.0)
        for tnode in self.tnodes.values():
            tnode.setValue(1.0)
        
    def getOutput(self):
        vals = []
        for o in self.inputs:
            vals.append(o.getValue())
        return vals

    def onInput(self):
        pass

    def addConnection(self, src, dest, weight=1.0):
        n1 = self.nodes.get(src)
        n2 = self.nodes.get(dest)
        if n1 and n2:
            self.connections[(n1, n2)] = Connection(n1, n2, weight, self.doprop)
        else:
            raise ConnectionError(n1, n2)

    def removeConnection(self, src, dest):
        n1 = self.nodes.get(src)
        n2 = self.nodes.get(dest)
        conn = self.connections.pop((n1, n2))
        self.nodes[src].outputs.remove(conn)
        self.nodes[dest].inputs.remove(conn)

    def addThreshold(self, destid, threshold):
        tnode = Node("%s threshold"%str(destid), self.doprop)
        tnode.outval = 1.0
        self.tnodes[tnode.id] = tnode
        dest = self.nodes.get(destid)
        if tnode and dest:
            self.connections[(tnode, dest)] = Connection(tnode, dest, threshold)
            dest.threshold = self.connections[(tnode, dest)]
            dest.threshold.setValue(1.0)
        else:
            raise ConnectionError(tnode, dest)

    def changeThreshold(self, dest, threshold):
        if self.nodes[dest].threshold:
            self.nodes[dest].threshold.weight = threshold
        else:
            raise KeyError("Node doesn't have a threshold")

    def changeWeight(self, src, dest, weight):
        n1 = self.nodes.get(src)
        n2 = self.nodes.get(dest)
        if n1 and n2:
            conn = self.connections[(n1, n2)]
            if conn:
                conn.changeWeight(weight)
            else:
                raise ConnectionError(n1, n2)
        else:
            raise ConnectionError(n1, n2)

    def addInput(self, dest, weight=1.0):
        n2 = self.nodes.get(dest)
        if n2:
            self.connections[(self, n2)] = Connection(self, n2, weight)
        else:
            raise ConnectionError(self, n2)

    def addOutput(self, src, weight=1.0):
        n1 = self.nodes.get(src)
        if n1:
            self.connections[(n1, self)] = Connection(n1, self, weight)
        else:
            raise ConnectionError(n1, self)

    def test(self, pattern):
        right = 0
        wrong = 0
        kap = {}
        for p in pattern:
            input = p[0]
            #print input, "->", 
            self.setInput(input)
            output = self.getOutput()
            for i in xrange(len(output)):
                if output[i] >= 0.5:
                    output[i] = 1
                else:
                    output[i] = 0
            #print output
            if p[1] == output:
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
        #print "right: %i, wrong: %i" % (right, wrong)
            #outstr = "["
            #for o in output:
            #    outstr += "%-.3f, "%o
            #outstr = outstr[:-2]
            #outstr += "]"
            #print outstr

class NodeDefinedError(Exception):
    def __init__(self, value):
        self.value = value
        print "Undefined Node: ", value
    def __str__(self):
        return repr(self.value)

class InputSizeError(Exception):
    def __init__(self):
        print "Input size doesn't match number of network inputs"

class ConnectionError(Exception):
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
        print "Cannot make a connection: %s %s"%(str(n1),str(n2))
    def __str__(self):
        return repr(self.n1) + ' ' + repr(self.n2)
