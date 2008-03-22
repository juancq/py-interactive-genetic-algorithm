def f1(*stats):

    roomDesc = stats[0]
    roomSizes = stats[1]
    roomClass = []
    area, revisedArea = [], []

    for k in range(0,len(roomSizes)):
        roomClass.append(float(roomSizes[k][2])-float(roomSizes[k][0]))
        roomClass.append(float(roomSizes[k][3])-float(roomSizes[k][1]))

    for k in range(0,len(roomSizes)):
        area.append(roomClass[2*k]*roomClass[2*k+1])

    for k in range(0,len(roomDesc)):
        if roomDesc[k] != 'S':
            revisedArea.append(area[k])

    return revisedArea
    
