def f1(*rooms):
    roomNum = rooms[0]
    roomDesc = rooms[1]
    roomSizes = rooms[2]

    roomListShare = {}
    
    for i in range(0,len(roomDesc)-1):
        if roomDesc[i] != 'S':
            roomOne = roomSizes[i]
            for j in range(i+1,len(roomDesc)):
                if roomDesc[j] != 'S':
                    roomTwo = roomSizes[j]

                    OneLines = [roomOne[1],roomOne[0],roomOne[3],roomOne[2]]
                    TwoLines = [roomTwo[1],roomTwo[0],roomTwo[3],roomTwo[2]]

                    count = 0
    
                    for k in range(0,len(OneLines)):
                        if k < 2:
                            if OneLines[k] == TwoLines[k+2]:
                                if k == 0:
                                    if roomTwo[0] >= roomOne[0] and roomTwo[0] < roomOne[2]:
                                        count = 1
                                        break
                                    elif roomTwo[0] <= roomOne[0] and roomTwo[2] > roomOne[0]:
                                        count = 1
                                        break
                                    else: count = 0
                                else:
                                    if roomTwo[1] >= roomOne[1] and roomTwo[1] < roomOne[3]:
                                        count = 1
                                        break
                                    elif roomTwo[1] <= roomOne[1] and roomTwo[3] > roomOne[1]:
                                        count = 1
                                        break
                                    else: count = 0
                            else: count = 0
                        else:
                            if OneLines[k] == TwoLines[k-2]:
                                if k == 2:
                                    if roomTwo[0] >= roomOne[0] and roomTwo[0] < roomOne[2]:
                                        count = 1
                                        break
                                    elif roomTwo[0] <= roomOne[0] and roomTwo[2] > roomOne[0]:
                                        count = 1
                                        break
                                    else: count = 0
                                else:
                                    if roomTwo[1] <= roomOne[1] and roomTwo[3] > roomOne[1]:
                                        count = 1
                                        break
                                    elif roomTwo[1] >= roomOne[1] and roomTwo[1] < roomOne[3]:
                                        count = 1
                                        break
                                    else: count = 0
                            else: count = 0

                    roomPair = roomDesc[i] + '-' + roomDesc[j]
                    roomListShare[roomPair] = count

    roomShare = []

    if roomNum == [0] or roomNum == [1]:
        roomShare = [0,0,0,0,0]
        
    elif roomNum == [2]:
        for roomPair in roomListShare.keys():
            if roomPair == 'LBK-RST' or roomPair == 'RST-LBK':
                adjacent = roomListShare[roomPair]
        roomShare = [adjacent, 1, 1, adjacent, adjacent]

    elif roomNum == [3]:
        for roomPair in roomListShare.keys():
            if roomPair == 'LKT-RST' or roomPair == 'RST-LKT':
                adjacent = roomListShare[roomPair]
        roomShare = [adjacent, 1, 1, adjacent]
        for roomPair in roomListShare.keys():
            if roomPair == 'BED-RST' or roomPair == 'RST-BED': roomShare.append(roomListShare[roomPair])

    elif roomNum == [4]:
        for roomPair in roomListShare.keys():
            if roomPair == 'LKT-RST' or roomPair == 'RST-LKT':
                adjacent = roomListShare[roomPair]
        roomShare = [adjacent, 1, 1, adjacent]
        
        for roomPair in roomListShare.keys():
            if roomPair == 'MBR-RST' or roomPair == 'RST-MBR':
                mbr_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'BED-RST' or roomPair == 'RST-BED':
                bed_rst = roomListShare[roomPair]

        if bed_rst or mbr_rst:
            roomShare.append(1)
        else:
            roomShare.append(0)

    elif roomNum == [5]:
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-RST' or roomPair == 'RST-LIV': roomShare.append(roomListShare[roomPair])
        roomShare.append(1)
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-KTH' or roomPair == 'KTH-LIV': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-RST' or roomPair == 'RST-KTH': roomShare.append(roomListShare[roomPair])

        for roomPair in roomListShare.keys():
            if roomPair == 'MBR-RST' or roomPair == 'RST-MBR':
                mbr_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'BED-RST' or roomPair == 'RST-BED':
                bed_rst = roomListShare[roomPair]

        if bed_rst or mbr_rst:
            roomShare.append(1)
        else:
            roomShare.append(0)

    elif roomNum == [6]:
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-RST' or roomPair == 'RST-LIV': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-DIN' or roomPair == 'DIN-LIV': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-DIN' or roomPair == 'DIN-KTH': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-RST' or roomPair == 'RST-KTH': roomShare.append(roomListShare[roomPair])

        for roomPair in roomListShare.keys():
            if roomPair == 'MBR-RST' or roomPair == 'RST-MBR':
                mbr_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'BED-RST' or roomPair == 'RST-BED':
                bed_rst = roomListShare[roomPair]

        if bed_rst or mbr_rst:
            roomShare.append(1)
        else:
            roomShare.append(0)

    elif roomNum == [7]:
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-RST' or roomPair == 'RST-LIV': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-DIN' or roomPair == 'DIN-LIV': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-DIN' or roomPair == 'DIN-KTH': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-RST' or roomPair == 'RST-KTH': roomShare.append(roomListShare[roomPair])

        for roomPair in roomListShare.keys():
            if roomPair == 'MBR-RST' or roomPair == 'RST-MBR':
                mbr_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'BED-RST' or roomPair == 'RST-BED':
                bed_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'GBR-RST' or roomPair == 'RST-GBR':
                gbr_rst = roomListShare[roomPair]

        if bed_rst or mbr_rst or gbr_rst:
            roomShare.append(1)
        else:
            roomShare.append(0)

    else:
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-RST' or roomPair == 'RST-LIV':
                liv_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-BTH' or roomPair == 'BTH-LIV':
                liv_bth = roomListShare[roomPair]

        if liv_rst or liv_bth:
            roomShare.append(1)
        else:
            roomShare.append(0)

        for roomPair in roomListShare.keys():
            if roomPair == 'LIV-DIN' or roomPair == 'DIN-LIV': roomShare.append(roomListShare[roomPair])
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-DIN' or roomPair == 'DIN-KTH': roomShare.append(roomListShare[roomPair])
   
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-RST' or roomPair == 'RST-KTH':
                kth_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'KTH-BTH' or roomPair == 'BTH-KTH':
                kth_bth = roomListShare[roomPair]

        if kth_rst or kth_bth:
            roomShare.append(1)
        else:
            roomShare.append(0)

        for roomPair in roomListShare.keys():
            if roomPair == 'MBR-RST' or roomPair == 'RST-MBR':
                mbr_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'BED-RST' or roomPair == 'RST-BED':
                bed_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'GBR-RST' or roomPair == 'RST-GBR':
                gbr_rst = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'MBR-BTH' or roomPair == 'BTH-MBR':
                mbr_bth = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'BED-BTH' or roomPair == 'BTH-BED':
                bed_bth = roomListShare[roomPair]
        for roomPair in roomListShare.keys():
            if roomPair == 'GBR-BTH' or roomPair == 'BTH-GBR':
                gbr_bth = roomListShare[roomPair]

        if bed_rst or mbr_rst or gbr_rst or bed_bth or mbr_bth or gbr_bth:
            roomShare.append(1)
        else:
            roomShare.append(0)
            
    return roomShare




