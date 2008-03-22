from common import *

def f1(roomDesc, roomSizes, revisedArea, roomClass):

    # One room Living Unit without Restroom facilities
    if len(revisedArea) == 1:                      
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                roomDesc[j] = 'LBK'                # LBK - Living/Bed/Kitchen Combo (w/o Restroom)
                break

    # Two room Apartment (Living Unit and Restroom)
    elif len(revisedArea) == 2:
        rst = 0
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                if rst == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[0]:
                    roomDesc[j] = 'RST'            # RST - Restroom
                    rst = 1
                else:
                    roomDesc[j] = 'LBK'            # LBK - Living/Bed/Kitchen Combo

    # Three room Apartment (Living Unit, Bedroom and Restroom) 
    elif len(revisedArea) == 3:
        rst, bed = 0, 0
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                if rst == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[0]:
                    roomDesc[j] = 'RST'            # RST - Restroom
                    rst = 1
                elif bed == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[1]:
                    roomDesc[j] = 'BED'            # BED - Bedroom
                    bed = 1
                else:
                    roomDesc[j] = 'LKT'            # LKT - Living/Kitchen Combo

    # Four room Apartment (Living Unit with 2 Bedrooms and Restroom)
    elif len(revisedArea) == 4:
        rst, mbr, bed = 0, 0, 0
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                if rst == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[0]:
                    roomDesc[j] = 'RST'            # RST - Restroom
                    rst = 1
                elif bed == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[1]:
                    roomDesc[j] = 'BED'            # BED - Bedroom
                    bed = 1
                elif mbr == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[2]:
                    roomDesc[j] = 'MBR'            # MBR - Master Bedroom
                    mbr = 1
                else:
                    roomDesc[j] = 'LKT'            # LKT - Living/Kitchen Combo

    # Five room Apartment (Living Room, 2 Bedrooms, Eat-In-Kitchen and Restroom)
    elif len(revisedArea) == 5:
        rst, kth, mbr, bed = 0, 0, 0, 0
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                if rst == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[0]:
                    roomDesc[j] = 'RST'            # RST - Restroom
                    rst = 1
                elif kth == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[1]:
                    roomDesc[j] = 'KTH'            # KTH - Kitchen/Dining Combo
                    kth = 1
                elif bed == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[2]:
                    roomDesc[j] = 'BED'            # BED - Bedroom
                    bed = 1
                elif mbr == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[3]:
                    roomDesc[j] = 'MBR'            # MBR - Master Bedroom
                    mbr = 1
                else:
                    roomDesc[j] = 'LIV'            # LIV - Living Room

    
    # Six room Apartment (Living Room, Dining Room, 2 Bedrooms, Kitchen and Restroom)
    elif len(revisedArea) == 6:
        rst, kth, mbr, bed, din = 0, 0, 0, 0, 0
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                if rst == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[0]:
                    roomDesc[j] = 'RST'            # RST - Rest Room
                    rst = 1
                elif kth == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[1]:
                    roomDesc[j] = 'KTH'            # KTH - Kitchen/Dining Combo
                    kth = 1
                elif bed == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[2]:
                    roomDesc[j] = 'BED'            # BED - Bed Room
                    bed = 1
                elif din == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[3]:
                    roomDesc[j] = 'DIN'            # DIN - Dining Room
                    din = 1
                elif mbr == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[4]:
                    roomDesc[j] = 'MBR'            # MBR - Master Bed Room
                    mbr = 1
                else:
                    roomDesc[j] = 'LIV'            # LIV - Living Room

    # Seven room Apartment (Living Room, Dining Room, 3 Bedrooms, Kitchen and Restroom)    
    elif len(revisedArea) == 7:
        rst, kth, mbr, gbr, bed, din = 0, 0, 0, 0, 0, 0
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                if rst == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[0]:
                    roomDesc[j] = 'RST'            # RST - Rest Room
                    rst = 1
                elif kth == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[1]:
                    roomDesc[j] = 'KTH'            # KTH - Kitchen/Dining Combo
                    kth = 1
                elif bed == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[2]:
                    roomDesc[j] = 'BED'            # BED - Bed Room
                    bed = 1
                elif gbr == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[3]:
                    roomDesc[j] = 'GBR'            # GBR - Guest Bed Room
                    gbr = 1
                elif din == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[4]:
                    roomDesc[j] = 'DIN'            # DIN - Dining Room
                    din = 1
                elif mbr == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[5]:
                    roomDesc[j] = 'MBR'            # MBR - Master Bed Room
                    mbr = 1
                else:
                    roomDesc[j] = 'LIV'            # LIV - Living Room

    # Eight or more rooms (Living Room, Dining Room, 2 Bedrooms, Kitchen and 2 Restrooms with other rooms if necessary)    
    else:
        rst, bth, kth, mbr, gbr, bed, din, liv = 0, 0, 0, 0, 0, 0, 0, 0
        for j in xrange(len(roomSizes)):
            if roomDesc[j] != 'S':
                if rst == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[0]:
                    roomDesc[j] = 'RST'            # RST - Rest Room
                    rst = 1
                elif bth == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[1]:
                    roomDesc[j] = 'BTH'            # BTH - Bath Room
                    bth = 1
                elif kth == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[2]:
                    roomDesc[j] = 'KTH'            # KTH - Kitchen/Dining Combo
                    kth = 1
                elif bed == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[len(revisedArea)-5]:
                    roomDesc[j] = 'BED'            # BED - Bed Room
                    bed = 1
                elif gbr == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[len(revisedArea)-4]:
                    roomDesc[j] = 'GBR'            # GBR - Guest Bed Room
                    gbr = 1
                elif din == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[len(revisedArea)-3]:
                    roomDesc[j] = 'DIN'            # DIN - Dining Room
                    din = 1
                elif mbr == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[len(revisedArea)-2]:
                    roomDesc[j] = 'MBR'            # MBR - Master Bed Room
                    mbr = 1
                elif liv == 0 and roomClass[2*j]*roomClass[2*j+1] == revisedArea[len(revisedArea)-1]:
                    roomDesc[j] = 'LIV'            # LIV - Living Room
                    liv = 1
                else:
                    roomDesc[j] = 'SRM'            # SRM - Some Room
    
    num_rooms = len(revisedArea)
    return roomDesc, num_rooms
