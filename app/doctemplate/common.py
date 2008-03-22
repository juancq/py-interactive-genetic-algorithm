#-------------------------------------------#
def roomArea(roomDesc, roomSizes):
    room_class = []
    revised_area = []

    for k in xrange(len(roomSizes)):
        temp1 = float(roomSizes[k][2])-float(roomSizes[k][0])
        temp2 = float(roomSizes[k][3])-float(roomSizes[k][1])
        print 'sizes: ', roomSizes[k]
        room_class.extend([temp1, temp2])
        if roomDesc[k] != 'S':
            revised_area.append(temp1*temp2)

    return revised_area, room_class
