from iga.individual import Individual
from iga.gacommon import gaParams

import parseTree, decodePlan, blockmaker

#-------------------------------------------#
class FloorplanIndividual(Individual):
    def __init__(self, random, params):
        self.params = params
        tree_genome = createInd.createIndividual(self.params['maxDepth'], self.params['maxRoom'], self.params['minRoom'])
        Individual.__init__(self, random, None, tree_genome)

        self.rank = 0
        self.crowded_distance = 0
        self.decodePlan()

#-------------------------------------------#
    def decodePlan(self):
        room_list = parseTree.parseTree(self, self.params['plotSizeX'],self.params['plotSizeY'])
        plan = decodePlan.decodePlan(room_list)

        self.decoded_plan = plan
        self.numRoom = plan[0]
        self.roomarea = plan[1]
        self.roomlist = plan[2]
        self.roomDesc = plan[3]
        self.roomSizes = plan[4]


#-------------------------------------------#
    def parseRoomList(room_list):

        rooms, roomDesc, roomSizes = [],[],[]
        roomarea, roomlist = [],[]
        
        # call the room-classification routine
        rooms = roomClassifier.f1(room_list)
        roomNum = rooms[-1:]
        rooms = rooms[:-1]

        numRoom = 0

        for k in xrange(0,len(rooms)/2):
            roomDesc.append(rooms[2*k])
            roomSizes.append(rooms[2*k+1])

        for k in xrange(len(roomDesc)):
            if roomDesc[k] != 'S':
                numRoom = numRoom + 1

        # call the area calculation routine
        roomarea = roomArea.f1(roomDesc,roomSizes)
        # call the adjoining-room calculation routine 
        roomlist = sharedWalls.f1(roomNum,roomDesc,roomSizes)

        return [numRoom, roomarea, roomlist, roomDesc, roomSizes]
