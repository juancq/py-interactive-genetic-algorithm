#-------------------------------------------#
class ShapeObject:
    def __init__(self, random, shape_type = 1, x = 0, y = 0, w = 0, l = 0, num_scale = 10):

        self.random = random
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.w = w
        self.l = l

        self.sx = 0
        self.sy = 0
        self.pos = 0

        self.img = None
        self.color = None
        self.text = None
        self.xscale_chrom = [random.randint(0, 1) for i in xrange(num_scale)]
        self.yscale_chrom = [random.randint(0, 1) for i in xrange(num_scale)]


        #self.sx = sx
        #self.sy = sy

#-------------------------------------------#
    def computePos(self, max_val = None, min_val = None):
        if max_val and min_val:
            self.max_val = max_val
            self.min_val = min_val
        else:
            max_val = self.max_val
            min_val = self.min_val

        # create transformation chromosomes on shapes
        xscale_chrom = self.xscale_chrom
        yscale_chrom = self.yscale_chrom
        len_scale = len(xscale_chrom)
        temp_x, temp_y = 0., 0.
        for j in xrange(len_scale):
            if xscale_chrom[j]:
                temp_x += 2**(len_scale-j-1)
            if yscale_chrom[j]:
                temp_y += 2**(len_scale-j-1)

        sx = temp_x/(2**len_scale)
        sy = temp_y/(2**len_scale)
        xdiff =  sx * (max_val-min_val) + min_val
        ydiff =  sy * (max_val-min_val) + min_val
        w = self.w - self.x
        l = self.l - self.y
        w = float(w) * xdiff * 0.5
        l = float(l) * ydiff * 0.5

        self.xdiff = w
        self.ydiff = l

#-------------------------------------------#
    def getArea(self):
        return (self.w * self.l)

#-------------------------------------------#
    def getPos(self):
        pos = self.x + self.xdiff, self.y + self.ydiff, self.w + self.xdiff, self.l + self.ydiff
        return pos

#-------------------------------------------#
    def reset(self, color):
        self.color = color
        self.img = None
        self.text = None

#-------------------------------------------#
    def setCenter(self, cx, cy):
        self.x = cx - self.w/2.
        self.y = cy - self.l/2.

#-------------------------------------------#
    def getCenter(self):
        cx = (self.x + (self.x + self.w))/2.
        cy = (self.y + (self.y + self.l))/2.
        return cx, cy

#-------------------------------------------#
    def mut(self, prob):

        random = self.random
        chrom = self.xscale_chrom
        for i in xrange(len(chrom)):
            if random.random() < prob:
                chrom[i] ^= 1

        chrom = self.yscale_chrom
        for i in xrange(len(chrom)):
            if random.random() < prob:
                chrom[i] ^= 1

        if random.random() < prob:
            self.shape_type = (self.shape_type + random.randrange(1, 4)) % 3 + 1


#-------------------------------------------#
    def xo(self, operator, other):

        c1Genome = copy.deepcopy(p1.genome['tree'])
        c2Genome = copy.deepcopy(p2.genome['tree'])

        # quad tree, so pick between 0 and 4
        b1, b2 = random.sample(range(0, 4), 2)
        
        branch1 = c1Genome[b1][:]
        branch2 = c2Genome[b2][:]
        c1Genome[b1] = branch2
        c2Genome[b2] = branch1

        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1.genome['tree'] = c1Genome
        c2.genome['tree'] = c2Genome

#-------------------------------------------#
    def scale(self, factor):
        self.x *= factor
        self.y *= factor
        self.w *= factor
        self.l *= factor
        self.computePos()

#-------------------------------------------#
    def printMe(self):
        print '-' * 30
        print 'obj: ', self.x, self.y, self.w, self.l

#-------------------------------------------#
