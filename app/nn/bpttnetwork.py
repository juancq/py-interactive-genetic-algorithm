from node import *
from connection import *
from funcs import dfunc
import random

class BackPropTTNetwork:
    def __init__(self, input, hidden, output, history, seed=0):
        """Create a 3-layer NN that uses backpropagation through time

        input (int) :: number of input nodes
        hidden (int) :: number of hidden nodes
        output (int) :: number of output nodes
        history (int) :: how many times steps to use for backprop
        seed (int) :: random number generator see
        """

        self.id = -1
        self.doprop = False
        self.layers = [[], [], []]
        self.inputs = []
        self.outputs = []
        self.tnode = Node("threshold", self.doprop)
        self.tnode.outval = 1.0
        self.history = history + 1 # The history also includes the current activation
        self.oldw = {} # Old weight changes used for momentum

        self.rand = random.Random()
        self.rand.seed(seed)
        for i in xrange(input):
            self.addToInputLayer()
        for i in xrange(hidden):
            self.addToHiddenLayer(self.rand.uniform(-1.0, 1.0))
        for i in xrange(output):
            self.addToOutputLayer(self.rand.uniform(-1.0, 1.0))

        # This connects all the hidden node together with recurrent links
        for i in self.layers[1]:
            for j in self.layers[1]:
                self.addConnection(i, j, self.rand.uniform(-1.0, 1.0), 1)

    def addToInputLayer(self):
        """Adds a node to the input layer"""
        newnode = self.addNode(0, squash=False)

        # Create a new connection between the network and the input node
        conn = Connection(self, newnode, 1.0, self.doprop)
        self.inputs.append(conn)
        newnode.inputs.append(conn)

    def addToOutputLayer(self, threshold):
        """Adds a node to the output layer
        
        threshold (float) :: the node's threshold weight
        """
        newnode = self.addNode(2, threshold)

        # Create a new connection between the network and the output node
        conn = Connection(newnode, self, 1.0, self.doprop)
        self.outputs.append(conn)
        newnode.outputs.append(conn)

    def addToHiddenLayer(self, threshold):
        """Adds a node to the hidden layer
        
        threshold (float) :: the node's threshold weight
        """
        newnode = self.addNode(1, threshold)

    def addNode(self, layer, threshold=None, squash=True):
        """Adds a node to the network and adds connections

        layer (int) :: which layer this node belongs, 0 - input, 1 - hidden, 2 - output
        threshold (float) :: A node's threshold weight. Optionally none for input nodes

        return newnode (Node) :: the new node created
        """
        id = (layer, len(self.layers[layer]))
        newnode = Node(id, self.doprop, self.history, squash)
        self.layers[layer].append(newnode)
        if threshold:
            self.addThreshold(newnode, threshold)
        if layer != 0: # Input nodes don't have predecessor nodes
            for n in self.layers[layer-1]:
                self.addConnection(n, newnode, self.rand.uniform(-2.0, 2.0))
        if layer != 2: # Output nodes don't have ancesstor nodes
            for n in self.layers[layer+1]:
                self.addConnection(newnode, n, self.rand.uniform(-2.0, 2.0))
        return newnode

    def addConnection(self, src, dest, weight=1.0, delay=0):
        """Adds a connection between two nodes

        src (Node) :: The source node
        dest (Node) :: The destination node
        weight (float) :: Optional (default 1.0). The weight of this connection
        delay (int) :: Optional (default 0). Recurrent links have values greater than 0.
                       This is how far back in time it gets its value. Right now this
                       has only been tested with values of 0 and 1.
        """
        conn = Connection(src, dest, weight, self.doprop, delay)
        src.outputs.append(conn)
        dest.inputs.append(conn)

    def addThreshold(self, dest, threshold):
        """Adds a threshold connection to the threshold node

        dest (Node) :: The destination node
        theshold (float) :: The weight of the threshold connection
        """
        conn = Connection(self.tnode, dest, threshold)
        self.tnode.outputs.append(conn)
        dest.inputs.append(conn)
        dest.threshold = self.tnode

    def setInput(self, vals):
        """Sets the inputs of the network to vals and propagates the values

        vals (list:float or ints) :: The input values

        Side effects: All the nodes and connections will likely have different
        values after this call
        
        After the values have been propagated, it takes the final activation of the hidden 
        nodes and pushes it on to the front of the queue and pops of the last of the
        queue. This is and important timing issue. When propagating the values, 
        the top of the queue will have the activation from one time step in the
        past. When backpropagating errors, the head of the queue will be the same as
        the current activation.

        """
        if len(vals) != len(self.inputs):
            print len(vals), len(self.inputs)
            raise InputSizeError # My own custom error! Pointless!

        for i in xrange(len(vals)):
            self.inputs[i].setValue(float(vals[i]))

        for layer in self.layers:
            for node in layer:
                node.onInput()

        for node in self.layers[1]:
            node.history.insert(0, node.outval)
            node.history.pop()

    def getOutput(self):
        """Returns a list of the output nodes activations"""
        vals = []
        for o in self.outputs:
            vals.append(o.getValue())
        return vals

    def test(self, pattern):
        """Tests the current network on the test data

        patterns (list or generator) :: It looks like this:
            [ 
                [ [list of inputs], [output list] ],
                ...more patterns...
            ]
            
            The generator should return a list (or tuple) of the input and output list:
            ([list of inputs], [list of outputs])

            At no point is the list modified, so the whole thing can be nested tuples
            if you like. The values of inputs and outputs can be floats or ints.

        returns (right, wrong, kap) (int, int, dict) ::
            right - number of correct guesses
            wrong - number of wrong guesses
            kap - a two dimentional kappa matrix (dictionary). Kappa not actually calulated

        Note: This is a fairly generic test function and may not work in many cases.
        For example, all the outputs are rounded to 1.0 or 0.0 which will only work
        if your sample outputs should be one or zero. It is easy to make your own
        test fuction. Just cycle through your own patterns, call setInput() and 
        getOutput() and do whatever calculations you like
        """
        right = 0
        wrong = 0
        kap = {}
        for p in pattern:
            input = p[0]
            self.setInput(input)
            output = [int(round(v)) for v in self.getOutput()]
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

    def train(self, patgen, rate, mrate, fi=None):
        """Trains a network for a given set of patterns

        patgen (Generator generator) :: Alright, let me explain,
            I use a generator function to create the set of patterns used in training.
            This is because when I created this thing, my test problem was predicting
            sine, with which I can easily generate points dynamically through a generator.
            The problem with a generator is when it is done generating, there isn't a way to
            reset it. Well, I can in python2.5, but 2.4 is still pretty prevalent. So, I need
            a way to generate pattern generators. It's kind of messy to explain, but looks
            good in code. Just look at the examples.
        rate (float) :: Learning rate
        mrate (float) :: Momentum rate
        fi (File) :: Optional. If specified, the epoch error will be dump to a files. 
                     Otherwise it is dumped to stdout.
        """
        self.epoch = 0
        for patterns in patgen:
            self.epoch += 1
            error = 0.0
            self.clear()
            self.patnum = 0
            for p in patterns:
                input = p[0]
                target = p[1]
                self.setInput(input)

                # We don't want to start adjusting weights until the history has been filled
                #if self.patnum > self.history:
                error += self.adjustWeights(target, rate, mrate)
                self.patnum += 1
            if fi:
                print >> fi, i, error
            else:
                print self.epoch, error

    def clear(self):
        for node in self.layers[1]:
            node.clear()

    def adjustWeights(self, target, rate, mrate):
        """Apply backpropagation through time on network and adjust weights

        target (list) :: the list of target outputs
        rate (float) :: learning rate
        mrate (float) :: momentum rate

        I don't think I can explain how backprop through time works here. There are
        papers and books for that. But I can explain my implementation and how it ties
        into the damned algorithm. 90% of this is standard backprop. Understanding that
        is probably a wise prequisite. I'll be mostly commenting on the "through time"
        parts. Read on!
        """
        outnodes = self.layers[2]
        if len(target) != len(outnodes):
            raise ValueError("wrong number of target values")

        # The keys are a tuple of the node and the time step for that delta (node, time). 
        # time = 0 is for the current time step. time > 0 is for back in time. It would
        # make more sense if time decreased, but it makes the programming a little easier.
        deltas = {}

        # Calculate output errors. Nothing different here.
        for k in xrange(len(target)):
            error = target[k] - outnodes[k].outval
            deltas[(outnodes[k],0)] = dfunc(outnodes[k].outval) * error
        
        # Calculate output error for hidden nodes at t = 0. Recurrent links aren't used for
        # this calculation. Except for that if statement, this is identical to regular
        # backprop. The reason that recurrent links aren't used is because it is important
        # to remember that hidden state layer and the hidden past state layer are really
        # "different" layers. The deltas at t = 0 only depend on the output layer. The 
        # state layer at t = 1 depends on the state layer at t = 0, t = 2 depends on t = 1, 
        # and so on. I hope this makes sense. BPTT is really confusing and hard to explain
        # without pictures. At least for me.
        for node in self.layers[1]:
            error = 0.0
            for conn in node.outputs:
                if conn.delay == 0:
                    error += deltas[(conn.dest, 0)] * conn.weight
            deltas[(node,0)] = dfunc(node.outval) * error

        # Now we can calculate deltas for older time steps. Because the t = 0 hidden 
        # layer relies on the output layer, unlike the t > 0 hidden layers that depend
        # on newer time hidden layers, it had to be calculated seperately. But now that we are
        # on the t > 0 hidden, we can iteratively move through the time steps. Notice that
        # this is for the most part identical to regular backprop, except now we keep moving
        # back in time (by increasing t (or i in this case)), the the dependent layer isn't
        # the output layer but hidden layer t - 1.
        
        # I'm assuming a delay of 1 here at all times. I should make it more general
        for i in xrange(self.history-1):
            for node in self.layers[1]:
                error = 0.0
                for conn in node.outputs:
                    if conn.delay == 1:
                        error += deltas[(conn.dest, i)] * conn.weight
                #I think this is right because hist[0] will be the same as node.outval
                #due to the way I store the history
                deltas[(node, i+1)] = dfunc(node.history[i+1]) * error

        # Now we can start changing weights. First the threshold nodes.
        for conn in self.tnode.outputs:
            change = deltas[(conn.dest,0)] * conn.weight * rate
            conn.weight += change
            conn.output = conn.weight

        # Now weight changes for the rest of the nodes. The weight changes for the recurrent
        # links are summed over each time step.
        for layer in self.layers:
            for node in layer:
                for conn in node.outputs:
                    if conn.dest.id != -1 and conn.src.id != -1:
                        if conn.delay == 0:
                            change = deltas[(conn.dest,0)] * conn.input * rate
                        elif conn.delay == 1:
                            change = 0.0
                            for i in xrange(self.history-1):
                                change += deltas[(conn.dest, i)] * conn.src.history[i+1] * rate
                        conn.weight += change + self.oldw.get(conn, 0.0) * mrate
                        self.oldw[conn] = change
        
        # find error - RMS
        error = 0.0
        N = len(target)
        for k in xrange(len(target)):
            error += 1.0/N * (target[k] - outnodes[k].outval)**2.0
        error = error ** 0.5
        return error


class InputSizeError(Exception):
    def __init__(self):
        print "Input size doesn't match number of network inputs"

class OutputSizeError(Exception):
    def __init__(self):
        print "Output size doesn't match number of network outputs"
