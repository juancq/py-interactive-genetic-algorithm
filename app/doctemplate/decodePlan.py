#!/usr/bin/env python

import roomClassifier, sharedWalls
from common import *

#-------------------------------------------#
def decodePlan(roomDesc, roomSizes):

    # call the room-classification routine
    roomDesc, numRoom = roomClassifier.f1(roomDesc, roomSizes)

    # call the area calculation routine
    roomarea, roomClass = roomArea(roomDesc,roomSizes)
    # call the adjoining-room calculation routine 
    shared_walls = sharedWalls.f1(numRoom,roomDesc,roomSizes)

    return [numRoom, roomarea, shared_walls, roomDesc, roomSizes]
