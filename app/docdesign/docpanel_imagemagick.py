import wx
import gui.feedbackpanel as feedbackpanel
from iga.gacommon import gaParams
from math import radians
from os import system

class DocMaker(feedbackpanel.FeedbackPanel):
    def __init__(self, parent, id, decoded_data, pos=wx.DefaultPosition, size=(300,300)):

        feedbackpanel.FeedbackPanel.__init__(self, parent, id, size)
        self.parent = parent
        self.SetBackgroundColour(wx.WHITE)
        self.SetMinSize(size)

        appVar = gaParams.getVar('application')
        self.width = size[0]
        self.height = size[1]

        self.decoded_data = decoded_data
        imgs = [wx.Image('app/docdesign/'+img) for img in appVar['images']]
        self.img_names = ['app/docdesign/'+img for img in appVar['images']]
        self.imgs = imgs

        self.Bind(wx.EVT_PAINT, self.draw)

#-------------------------------------------#
    def getBmpMagick(self, img, i):
        '''
        Return a bitmap corresponding to the room type.
        '''
        x = self.decoded_data['x_%d' % i]
        y = self.decoded_data['y_%d' % i]
        s = self.decoded_data['s_%d' % i]
        r = self.decoded_data['r_%d' % i]
        #tmp_img = img.Copy()

        name = self.img_names[i]
        new_name = '%s__temp__.png' % name
        system('convert -background None -bordercolor None -rotate %f %s %s' % (r, name, new_name))
        tmp_img = wx.Image(new_name)

        #tmp_img.SetMaskColour(255, 255, 255)

        width, height = tmp_img.GetSize()
        tmp_img.Rescale(s*width, s*height)

        width, height = tmp_img.GetSize()
        tmp_img.Rescale(width/3., height/3.)
        #tmp_img = tmp_img.Rotate(radians(r), (0,0))

        #tmp_img.ConvertColourToAlpha(255, 255, 255)

        x = int(x * self.width)
        y = int(y * self.height)
        return tmp_img.ConvertToBitmap(), [x, y]

#-------------------------------------------#
    def getBmp(self, img, i):
        '''
        Return a bitmap corresponding to the room type.
        '''
        x = self.decoded_data['x_%d' % i]
        y = self.decoded_data['y_%d' % i]
        s = self.decoded_data['s_%d' % i]
        r = self.decoded_data['r_%d' % i]
        #tmp_img = img.Copy()

        name = self.img_names[i]
        new_name = '%s__temp__.png' % name
        system('convert -background None -bordercolor None -rotate %f %s %s' % (r, name, new_name))
        tmp_img = wx.Image(new_name)

        #tmp_img.SetMaskColour(255, 255, 255)

        width, height = tmp_img.GetSize()
        tmp_img.Rescale(s*width, s*height)

        width, height = tmp_img.GetSize()
        tmp_img.Rescale(width/3., height/3.)
        #tmp_img = tmp_img.Rotate(radians(r), (0,0))

        #tmp_img.ConvertColourToAlpha(255, 255, 255)

        x = int(x * self.width)
        y = int(y * self.height)
        return tmp_img.ConvertToBitmap(), [x, y]


#-------------------------------------------#
    def draw(self, event):
        '''
        Draw collage.
        '''
        dc = wx.PaintDC(self)

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        dc.SetPen(wx.Pen("black",2))
        dc.DrawRectangle(10, 5, self.width, self.height)
        #dc.SetPen(wx.Pen("black",1))

        i = 0
        for img in self.imgs:
            pic, coords = self.getBmp(img, i)
            dc.DrawBitmap(pic, coords[0], coords[1])
            i += 1

#-------------------------------------------#
