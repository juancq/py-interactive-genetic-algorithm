import wx
import gui.feedbackpanel as feedbackpanel
from iga.gacommon import gaParams
from testtemplate import TestTemplate

class DocPanel(feedbackpanel.FeedbackPanel):
    def __init__(self, parent, ID=wx.NewId(), dimensions=[], description=[], transf = [], color_scheme = [], pos=wx.DefaultPosition, size=(220,260)):
        feedbackpanel.FeedbackPanel.__init__(self,parent,ID,size)

        self.parent = parent
        self.SetBackgroundColour(wx.WHITE)
        self.dimensions=dimensions
        self.description=description
        self.transf = transf
        self.color_scheme = color_scheme

        self.coordinates, self.roomsizes = self.getRoomDesc()

        self.SetMinSize(size)

        appVar = gaParams.getVar('application')
        self.max_val = appVar['max_scale']
        self.min_val = appVar['min_scale']
        self.rr_radius = appVar['rr_radius']


        self.width = appVar['plotSizeX']
        self.height = appVar['plotSizeY']
        self.canvas = wx.Panel(self, size =(self.width, self.height))
        self.canvas.Bind(wx.EVT_PAINT, self.draw)
        
        vsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.AddSpacer((20,10))
        vsizer.Add(self.canvas)


        test_bmp = wx.Bitmap('app/doctemplate/eog.png')
        test_button = wx.BitmapButton(self, wx.NewId(), bitmap = test_bmp)
        self.Bind(wx.EVT_BUTTON, self.onTest, test_button)

        vsizer.AddSpacer((10,10))
        vsizer.Add(test_button)

        self.sizer.Add(vsizer)

        self.computeShapeLoc()

#-------------------------------------------#
    def onTest(self, event):
        template = TestTemplate(self, self.coordinates, self.roomsizes, 
                         self.color_scheme, self.transf, self.rr_radius,
                         (self.width, self.height))
        template.Show()

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
        #xoffset = 25.0
        #yoffset = 40.0
        xoffset = 0.0
        yoffset = 0.0

        for i in xrange(0, len(self.dimensions)):
            coordinates.append(float(self.dimensions[i][0])+xoffset)
            coordinates.append(float(self.dimensions[i][1])+yoffset)
            roomsizes.append(float(self.dimensions[i][2])-float(self.dimensions[i][0]))
            roomsizes.append(float(self.dimensions[i][3])-float(self.dimensions[i][1]))

        return coordinates, roomsizes

#-------------------------------------------#
    def computeShapeLoc(self):
        '''
        Compute the coordinates and sizes of all shapes.
        '''
        shape_list = []
        coordinates, shape_sizes = self.coordinates, self.roomsizes
        i = 0
        transf = self.transf
        max_val = self.max_val
        min_val = self.min_val

        color = self.color_scheme
        len_color = len(color)

        shape_i = 0
        for j in xrange(len(self.transf)):

            # if not a blank space
            shape = transf[j][-1]
            if shape:
                shape_i += 1
                c = color[shape_i % len_color]
                xdiff =  transf[j][0] * (max_val-min_val) + min_val
                ydiff =  transf[j][1] * (max_val-min_val) + min_val
                l = shape_sizes[i] - coordinates[i]
                w = shape_sizes[i+1] - coordinates[i+1]
                l = float(l) * xdiff * 0.5
                w = float(w) * ydiff * 0.5

                shape_list.append({'shape': shape, 'img': None,
                        'color': c, 'text': None, 
                        'pos':[coordinates[i]+l, coordinates[i+1]+w, 
                        shape_sizes[i]+l, shape_sizes[i+1]+w]})
            i += 2

        self.shape_list = shape_list


#-------------------------------------------#
    def draw(self, event):
        '''
        Draw the document with various shapes, but no overlap (ignore x and y
        deformation values).
        '''
        dc = wx.PaintDC(self.canvas)
        dc.SetBackground(wx.Brush(wx.WHITE))
        dc.Clear()
        dc.SetPen(wx.Pen("black",1))

        coordinates, roomsizes = self.coordinates, self.roomsizes
        color = self.color_scheme
        len_color = len(color)
        i = 0
        for obj in self.shape_list:

            shape = obj['shape']
            c1, c2, c3, c4 = obj['pos']
            i += 1

            c = obj['color']
            dc.SetBrush(wx.Brush(c))
            if shape == 1:
                dc.DrawRectangle(c1, c2, c3, c4)
            elif shape == 2:
                dc.DrawRoundedRectangle(c1, c2, c3, c4, self.rr_radius)
            elif shape == 3:
                dc.DrawEllipse(c1, c2, c3, c4)


        dc.SetPen(wx.Pen("black",4))
        dc.DrawLineList([(coordinates[0], coordinates[1], self.width, coordinates[1]), 
                (self.width, coordinates[1], self.width, self.height),
                (self.width, self.height, coordinates[0], self.height),
                (coordinates[0], self.height, coordinates[0], coordinates[1])]
                )

#-------------------------------------------#
    def drawNoOverlap(self, event):
        '''
        Draw the document with various shapes, but no overlap (ignore x and y
        deformation values).
        '''
        dc = wx.PaintDC(self)
        coordinates, roomsizes = self.coordinates, self.roomsizes

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        dc.SetPen(wx.Pen("black",2))
        dc.DrawRectangle(coordinates[0], coordinates[1], self.width, self.height)

        transf = self.transf
        max_val = 5.
        min_val = -5.
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

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                dc.SetBrush(wx.Brush('yellow'))           

            # Other rooms
            else:
                dc.SetBrush(wx.Brush('dim gray'))         

            # if not a blank space
            shape = transf[j][-1]
            if shape:
                xdiff =  transf[j][0] * (max_val-min_val) + min_val
                ydiff =  transf[j][1] * (max_val-min_val) + min_val
                if shape == 1:
                    dc.DrawRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])
                elif shape == 2:
                    dc.DrawRoundedRectangle(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1], 5.)
                elif shape == 3:
                    dc.DrawEllipse(coordinates[i], coordinates[i+1], roomsizes[i], roomsizes[i+1])

            i += 2

#-------------------------------------------#
