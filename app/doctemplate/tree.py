from copy import deepcopy
from shape import ShapeObject

#-------------------------------------------#
class Tree:
    def __init__(self, random, size_x, size_y):

        self.random = random
        self.branch = [[], [], [], []]
        self.size_x = size_x
        self.size_y = size_y

        self.cx = size_x / 2.
        self.cy = size_y / 2.

#-------------------------------------------#
    def randCenter(self, b1, branch1, min_len, len_b1):
        '''
        Assign random centers to shapes that fall on new quadrant.
        '''
        random = self.random
        xoffset, yoffset = 0., 0.
        if b1 == 1:
            xoffset = self.cx
        elif b1 == 2:
            yoffset = self.cy
        elif b1 == 3:
            xoffset = self.cx
            yoffset = self.cy

        for i in xrange(min_len, len_b1):
            cx_rand = random.random()
            cx_rand *= self.cx
            cy_rand = random.random()
            cy_rand *= self.cy
            branch1[i].setCenter(cx_rand + xoffset, cy_rand + yoffset)


#-------------------------------------------#
    def randNodeCenter(self, b1, node):
        random = self.random
        xoffset, yoffset = 0., 0.
        if b1 == 1:
            xoffset = self.cx
        elif b1 == 2:
            yoffset = self.cy
        elif b1 == 3:
            xoffset = self.cx
            yoffset = self.cy

        cx_rand = random.random()
        cx_rand *= self.cx
        cy_rand = random.random()
        cy_rand *= self.cy
        node.setCenter(cx_rand + xoffset, cy_rand + yoffset)


#-------------------------------------------#
    def getAnyNode(self):

        for branch in self.branch:
            if branch:
                return branch[0]

#-------------------------------------------#
    def addNode(self):
        random = self.random
        b1 = random.randrange(0, 4)
        branch = self.branch[b1]

        xoffset, yoffset = 0., 0.
        if b1 == 1:
            xoffset = self.cx
        elif b1 == 2:
            yoffset = self.cy
        elif b1 == 3:
            xoffset = self.cx
            yoffset = self.cy

        cx_rand = random.random()
        cx_rand *= self.cx
        cy_rand = random.random()
        cy_rand *= self.cy
        node = deepcopy(self.getAnyNode())
        node.setCenter(cx_rand + xoffset, cy_rand + yoffset)
        branch.append(node)


#-------------------------------------------#
    def deleteNode(self):
        random = self.random
        branch = self.branch[random.randrange(0, 4)]
        if branch:
            i = random.randrange(0, len(branch))
            del branch[i]

#-------------------------------------------#
    def cloneNode(self):
        random = self.random
        b1, b2 = random.sample(range(0, 4), 2)
        branch1, branch2 = self.branch[b1], self.branch[b2]
        if branch1:
            i = random.randrange(0, len(branch1))
            clone = deepcopy(branch1[i])
            branch2.append(clone)
            self.randNodeCenter(b2, clone)

        elif branch2:
            i = random.randrange(0, len(branch2))
            clone = deepcopy(branch2[i])
            branch1.append(clone)
            self.randNodeCenter(b1, clone)

#-------------------------------------------#
    def quadrantSwap(self, b1, other_branch):

        branch1 = self.branch[b1]

        len_b1 = len(branch1)
        len_b2 = len(other_branch)
        min_len = min(len_b1, len_b2)

        for i in xrange(min_len):
            cx_1, cy_1 = branch1[i].getCenter()
            cx_2, cy_2 = other_branch[i]
            branch1[i].setCenter(cx_2, cy_2)

        if branch1:
            self.randCenter(b1, branch1, min_len, len_b1)

#-------------------------------------------#
    def rearrange(self):
        #print 'tree ', '-'*30
        #for b in self.branch:
        #    print 'branch: ', len(b)

        new_tree = [[], [], [], []]
        for branch in self.branch:
            for shape in branch:
                cx, cy = shape.getCenter()
                if cx < self.cx and cy < self.cy:
                    new_tree[0].append(shape)
                elif cx >= self.cx and cy < self.cy:
                    new_tree[1].append(shape)
                elif cx < self.cx and cy >= self.cy:
                    new_tree[2].append(shape)
                elif cx >= self.cx and cy >= self.cy:
                    new_tree[3].append(shape)

        self.branch = new_tree
        #print 'tree ', '-'*30
        #for b in self.branch:
        #    print 'branch: ', len(b)

#-------------------------------------------#
