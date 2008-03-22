import wx
import gui.feedbackpanel as feedbackpanel
from iga.gacommon import gaParams

class BlockMaker(feedbackpanel.FeedbackPanel):
    def __init__(self,parent,ID=-1,dimensions=[],description=[],pos=wx.DefaultPosition,size=(220,260)):
        feedbackpanel.FeedbackPanel.__init__(self,parent,ID,size)

        self.parent = parent
        self.SetBackgroundColour(wx.WHITE)
        self.dimensions=dimensions
        self.description=description
        self.SetMinSize(size)

        appVar = gaParams.getVar('application')
        self.width = appVar['plotSizeX']
        self.height = appVar['plotSizeY']

        rooms = {}
        rooms['bath'] = wx.Image('app/floorplanner/bath.png')
        rooms['bedroom'] = wx.Image('app/floorplanner/bedroom.png')
        rooms['kitchen'] = wx.Image('app/floorplanner/kitchen.png')
        rooms['livingroom'] = wx.Image('app/floorplanner/livingroom.png')
        self.rooms = rooms

        if appVar.has_key('texture') and appVar['texture']:
            self.Bind(wx.EVT_PAINT, self.drawWithTextures)
        else:
            self.Bind(wx.EVT_PAINT, self.drawWithColor)
              

#-------------------------------------------#
    def getRoom(self, room_type, x, y):
        '''
        Return a bitmap corresponding to the room type.
        '''
        tmp_room = self.rooms[room_type].Copy()
        tmp_room.Rescale(x, y)

        return tmp_room.ConvertToBitmap()


#-------------------------------------------#
    def getRoomDesc(self):
        coordinates = []
        roomsizes = []
        xoffset = 25.0
        yoffset = 40.0

        for i in xrange(0, len(self.dimensions)):
            coordinates.append(float(self.dimensions[i][0])+xoffset)
            coordinates.append(float(self.dimensions[i][1])+yoffset)
            roomsizes.append(float(self.dimensions[i][2])-float(self.dimensions[i][0]))
            roomsizes.append(float(self.dimensions[i][3])-float(self.dimensions[i][1]))

        return coordinates, roomsizes

#-------------------------------------------#
    def drawWithColor(self, event):
        '''
            Draw the floorplan rooms using a different color for each room.
        '''
        dc = wx.PaintDC(self)
        coordinates, roomsizes = self.getRoomDesc()

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        dc.SetPen(wx.Pen("black",2))
        dc.DrawRectangle(coordinates[0], coordinates[1], self.width, self.height)
        i = 0

        dc.SetPen(wx.Pen("black",1))

        for j in xrange(0, len(self.dimensions)):
            if self.description[j] == 'S':
                dc.SetBrush(wx.Brush('white'))

            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif self.description[j] == 'RST' or self.description[j] == 'BTH':
                dc.SetBrush(wx.Brush('firebrick'))        

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif self.description[j] == 'KTH' or self.description[j] == 'DIN':
                dc.SetBrush(wx.Brush('green'))            

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif self.description[j] == 'LIV' or self.description[j] == 'LBK' or self.description[j] == 'LKT':
                dc.SetBrush(wx.Brush('red'))              
                #dc.DrawRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                dc.SetBrush(wx.Brush('yellow'))           

            # Other rooms
            else:
                dc.SetBrush(wx.Brush('dim gray'))         

            dc.DrawRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])
            #dc.DrawRoundedRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1], 5.)
            #dc.DrawEllipse(coordinates[i], coordinates[i+1], roomsizes[i]-10, roomsizes[i+1])

            i += 2

#-------------------------------------------#
    def drawWithTextures(self, event):
        '''
        Draw the floorplan rooms using textures.
        '''
        dc = wx.PaintDC(self)
        coordinates, roomsizes = self.getRoomDesc()

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        dc.SetPen(wx.Pen("black",2))
        dc.DrawRectangle(coordinates[0], coordinates[1], self.width, self.height)
        i = 0

        dc.SetPen(wx.Pen("black",1))

        for j in xrange(0, len(self.dimensions)):
            if self.description[j] == 'S':
                dc.SetBrush(wx.Brush('white'))
                dc.DrawRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])

            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif self.description[j] == 'RST' or self.description[j] == 'BTH':
                dc.SetBrush(wx.Brush('firebrick'))        
                room = self.getRoom('bath', roomsizes[i], roomsizes[i+1])
                dc.DrawBitmap(room, coordinates[i], coordinates[i+1])

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif self.description[j] == 'KTH' or self.description[j] == 'DIN':
                dc.SetBrush(wx.Brush('green'))            
                room = self.getRoom('kitchen', roomsizes[i], roomsizes[i+1])
                dc.DrawBitmap(room, coordinates[i], coordinates[i+1])

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif self.description[j] == 'LIV' or self.description[j] == 'LBK' or self.description[j] == 'LKT':
                dc.SetBrush(wx.Brush('red'))              
                room = self.getRoom('livingroom', roomsizes[i], roomsizes[i+1])
                dc.DrawBitmap(room, coordinates[i], coordinates[i+1])

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                dc.SetBrush(wx.Brush('yellow'))           
                room = self.getRoom('bedroom', roomsizes[i], roomsizes[i+1])
                dc.DrawBitmap(room, coordinates[i], coordinates[i+1])

            # Other rooms
            else:
                dc.SetBrush(wx.Brush('dim gray'))         
                dc.DrawRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])

            i += 2

#-------------------------------------------#
