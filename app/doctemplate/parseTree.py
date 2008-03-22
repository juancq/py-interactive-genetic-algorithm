
class tree_node:
    def __init__(self,orientation,percent,childOne=None,childTwo=None):
        self.orientation = orientation
        self.percent = percent
        self.childOne = childOne
        self.childTwo = childTwo

def traverse(node,startx,starty,length,height):
    results = []
    if not node.childOne and not node.childTwo:
        results.append( (startx,starty,startx+length,starty+height) )
    else:
        if node.orientation == 1:
            top_startx = startx
            top_starty = starty
            top_length = length
            top_height = height*node.percent
            bottom_startx = top_startx
            bottom_starty = top_starty + top_height
            bottom_length = length
            bottom_height = height - top_height
            if node.childOne:
                results.extend(traverse(node.childOne,top_startx,top_starty,top_length,top_height))
            if node.childTwo:
                results.extend(traverse(node.childTwo,bottom_startx,bottom_starty,bottom_length,bottom_height))
        elif node.orientation == 2:
            left_startx = startx
            left_starty = starty
            left_length = length*node.percent
            left_height = height
            right_startx = startx + left_length
            right_starty = starty
            right_length = length - left_length
            right_height = height
            if node.childOne:
                results.extend(traverse(node.childOne,left_startx,left_starty,left_length,left_height))
            if node.childTwo:
                results.extend(traverse(node.childTwo,right_startx,right_starty,right_length,right_height))

    return results


def parseTree(tree, plotSizeX, plotSizeY):

    plan = []
    plan.append(tree[0])
    tree = tree[1:]
    
    curpos = []
    termconditions = []
    global termCond 
    global currInLine
    global currLine
    global currLoc

    termCond = []
    currInLine = []

    def reclosefunc():

        global currInLine
        global currLine
        global currLoc
        global termCond

        currInLine[currLine][currLoc] = 2
        if currInLine != termCond:
            if currLoc % 2 != 0:
                currLine = currLine - 1
                for i in xrange(len(tree[currLine])):
                    if currInLine[currLine][i] == 1:
                        currLoc = i
                        reclosefunc()
                        break
                        
            else:
                currLoc = currLoc + 1

    for i in xrange(len(tree)):
        for j in xrange(len(tree[i])):
            curpos.append(0)
            termconditions.append(2)
        currInLine.append(curpos)
        termCond.append(termconditions)
        curpos = []
        termconditions = []

    currLine = 0
    currLoc = currInLine[currLine][0]
                
    while (currInLine != termCond):
        currInLine[currLine][currLoc] = 1
        plan.append(tree[currLine][currLoc])

        if tree[currLine][currLoc][1] == 1.0 or tree[currLine][currLoc][1] == 0.0:
            reclosefunc()    
        else:
            currLine = currLine + 1
            for i in xrange(len(tree[currLine])):
                if currInLine[currLine][i] == 0:
                    currLoc = i
                    break

    plotRooms = []
    plotElements = [(0,0,plotSizeX,plotSizeY)]
    roomDesc = []

    for i in xrange(len(plan)):
        if plan[i][1] != 1.0 and plan[i][1] != 0.0:
            tree = tree_node(plan[i][0],plan[i][1],tree_node(1,1,None,None),tree_node(1,1,None,None))
            plotDivision = traverse(tree,plotElements[0][0],plotElements[0][1],plotElements[0][2]-plotElements[0][0],plotElements[0][3]-plotElements[0][1])
            plotElements.insert(1,plotDivision[0])
            plotElements.insert(2,plotDivision[1])
            del plotElements[0]
        else:
            if plan[i][1] == 1.0:
                roomDesc.append('R')
                # create a list of new parameters, including x and y deformations
                # and shape type
            else:
                roomDesc.append('S')

            plotRooms.append(plotElements[0])
            del plotElements[0]


    return {'sizes': plotRooms, 'desc': roomDesc}
