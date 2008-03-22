def roomArea(roomDesc, roomSizes):
    room_class = []

    len_roomsize = len(roomSizes)
    for k in xrange(len_roomsize):
        room_class.append(float(roomSizes[k][2])-float(roomSizes[k][0]))
        room_class.append(float(roomSizes[k][3])-float(roomSizes[k][1]))

    area = [room_class[2*k]*room_class[2*k+1] for k in xrange(len_roomsize)]
    revised_area = [area[k] for k in xrange(len(roomDesc)) if roomDesc[k] != 'S']

    return revised_area, room_class
