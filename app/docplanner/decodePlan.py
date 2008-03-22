#!/usr/bin/env python

import roomClassifier
import sharedWalls#, roomArea
from common import *

#-------------------------------------------#
def decodePlan(roomDesc, roomSizes):

    # call the room-classification routine
    roomDesc, numRoom = roomClassifier.f1(roomDesc, roomSizes)

    ## count number of rooms, long way
    #numRoom = 0
    #for k in xrange(len(roomDesc)):
    #    if roomDesc[k] != 'S':
    #        numRoom = numRoom + 1
    ## count number of rooms
    #v = len(roomDesc) - roomDesc.count('S')

    # call the area calculation routine
    roomarea, roomClass = roomArea(roomDesc,roomSizes)
    # call the adjoining-room calculation routine 
    sharedwalls_roomlist = sharedWalls.f1(numRoom,roomDesc,roomSizes)

    return [numRoom, roomarea, sharedwalls_roomlist, roomDesc, roomSizes]

