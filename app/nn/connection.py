class Connection:
    def __init__(self, src, dest, weight=1.0, doprop=True, delay=0):
        self.input = 0.0
        self.output = 0.0
        self.weight = float(weight)
        #src.outputs.append(self)
        #dest.inputs.append(self)
        self.src = src
        self.dest = dest
        self.dirty = False
        self.dest = dest
        self.doprop = doprop
        self.delay = delay

    def setValue(self, value):
        self.input = value
        self.output = value * self.weight
        self.dirty = True
        if self.doprop:
            self.dest.onInput()

    def getValue(self):
        #self.output = self.input * self.weight
        if self.delay == 0:
            return self.output
        else:
            return self.weight * self.src.history[self.delay-1]

    def clear(self):
        self.dirty = False

    def updateWeight(self, delta):
        self.weight += delta
        self.output = self.input*self.weight
    
    def changeWeight(self, weight):
        self.weight = float(weight)
        if self.input != None:
            self.output = self.input*self.weight

    def __str__(self):
        return "%s -> %s" % (str(self.src.id), str(self.dest.id))

    def __repr__(self):
        return str(self)
