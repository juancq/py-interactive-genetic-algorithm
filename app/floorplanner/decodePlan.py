#!/usr/bin/env python

import roomClassifier
import roomArea
import sharedWalls

def decodePlan(room_list):

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
