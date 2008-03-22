import wx
import gui.feedbackpanel as feedbackpanel
from iga.gacommon import gaParams
from testtemplate import TestTemplate
from copy import deepcopy

class DocPanel(feedbackpanel.FeedbackPanel):
    def __init__(self, parent, ID=wx.NewId(), individual = None, quad_tree=[], color_scheme = [], pos=wx.DefaultPosition, size=(220,260)):
        feedbackpanel.FeedbackPanel.__init__(self,parent,ID,size)

        self.parent = parent
        self.SetBackgroundColour(wx.WHITE)
        self.shape_list = quad_tree
        self.color_scheme = color_scheme
        self.rank = individual.rank
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

        self.updateShapeList()
        self.sizer.Add(wx.StaticText(self, -1, 'R: %d' % self.rank))


#-------------------------------------------#
    def onTest(self, event):
        template = TestTemplate(self, deepcopy(self.shape_list),
                         self.color_scheme, self.rr_radius,
                         (self.width, self.height))
        template.Show()


#-------------------------------------------#
    def updateShapeList(self):

        color = self.color_scheme
        len_color = len(color)
        i = 0
        for obj in self.shape_list:
            c = color[i % len_color]
            obj.reset(c)
            i += 1


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

        for obj in self.shape_list:

            shape = obj.shape_type
            c1, c2, c3, c4 = obj.getPos()
            c = obj.color
            dc.SetBrush(wx.Brush(c))
            if shape == 1:
                dc.DrawRectangle(c1, c2, c3, c4)
            elif shape == 2:
                dc.DrawRoundedRectangle(c1, c2, c3, c4, self.rr_radius)
            elif shape == 3:
                dc.DrawEllipse(c1, c2, c3, c4)

        dc.SetPen(wx.Pen("black",4))
        dc.DrawLineList([(0, 0, self.width, 0), 
                (self.width, 0, self.width, self.height),
                (self.width, self.height, 0, self.height),
                (0, self.height, 0, 0)]
                )

#-------------------------------------------#
