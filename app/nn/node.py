from funcs import sfunc

class Node:
    def __init__(self, id, doprop=True, history=0, squash=True):
        self.id = id
        self.outputs = []
        self.inputs = []
        self.outval = None
        self.oninputs = 0
        self.threshold = None
        self.doprop = doprop
        self.history = [0] * history
        self.histlen = history
        self.squash = squash

    def clear(self):
        self.history = [0] * self.histlen

    def setValue(self, value):
        self.outval = value
        for o in self.outputs:
            if o:
                o.input = self.outval
                o.output = self.outval * o.weight
                o.dirty = True
                if o.doprop:
                    o.dest.onInput()
                #o.setValue(self.outval)

    def onInput(self):
        allSet = True
        if self.doprop:
            for i in self.inputs:
                if not i.dirty:
                    allSet = False
        if allSet:
            sum = 0.0
            #print self.id,
            for i in self.inputs:
                sum += i.getValue()
                #sum += i.output
                if self.doprop:
                    i.clear()
            #print "=", sum,
            if self.squash:
                self.outval = sfunc(sum)
            else:
                self.outval = sum
            #print "->", self.outval
            for o in self.outputs:
                if o.delay == 0:
                    o.input = self.outval
                    o.output = self.outval * o.weight
                    o.dirty = True
                    if o.doprop:
                        o.dest.onInput()
                    #o.setValue(self.outval)
