
import wx
from tooldlg import InsertDialog

class TestTemplate(wx.Frame):

    def __init__(self, parent, shape_list, color_scheme, 
            rr_radius, panel_size):

        self.parent = parent
        self.scale_factor = scale_factor = 3
        self.width = panel_size[0] * scale_factor
        self.height = panel_size[1] * scale_factor
        wx.Frame.__init__(self, None, wx.NewId(), size=(self.width, self.height))
        self.SetTitle('Test Template')

        #self.shape_sizes = shape_sizes
        self.color_scheme = color_scheme
        self.rr_radius = rr_radius * scale_factor

        self.shape_list = shape_list
        self.updateShapeList()
        self.drawHiddenBmp()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas = wx.Panel(self, size =(self.width, self.height))
        self.canvas.Bind(wx.EVT_PAINT, self.draw)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.onClickBar)
        
        vsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.Add(self.canvas)
        self.sizer.Add(vsizer)

        self.SetSizer(self.sizer)


#-------------------------------------------#
    def onClick(self, event):
        '''
        Determine shape clicked, then ask the user to 
        choose an image to replace current shape.
        '''
        dc = wx.MemoryDC()
        dc.SelectObject(self.hidden_canvas)

        pos = event.GetPosition()
        color = dc.GetPixelPoint(pos)

        i = color.Red()
        if i < 255:

            # Ask the user to load an image to replace selected shape
            dirname = ''
            dlg = wx.FileDialog(self, "Insert Image", dirname, "", 'All files (*)|*|PNG (*png)|*png', wx.OPEN)

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                img = self.createWxImage(path, self.shape_list[i])
                self.shape_list[i]['img'] = img

            dlg.Destroy()

        self.Refresh()

#-------------------------------------------#
    def onClickBar(self, event):
        '''
        Determine shape clicked, then ask the user to 
        choose an image to replace current shape.
        '''
        dc = wx.MemoryDC()
        dc.SelectObject(self.hidden_canvas)

        pos = event.GetPosition()
        color = dc.GetPixelPoint(pos)

        i = color.Red()
        if i < 255:

            # Ask the user to load an image to replace selected shape
            dirname = ''
            dlg = InsertDialog(self, self.shape_list[i].getPos())

            if dlg.ShowModal() == wx.ID_OK:
                if dlg.image:
                    path = dlg.image
                    img = self.createWxImage(path, self.shape_list[i])
                    self.shape_list[i].img = img
                elif dlg.text:
                    text = dlg.text
                    self.shape_list[i].text = text
                elif dlg.color:
                    c = dlg.color
                    self.shape_list[i].color = c


            dlg.Destroy()

        self.Refresh()

#-------------------------------------------#
    def createWxImage(self, name, shape_info):
        shape = shape_info.shape_type
        c1, c2, c3, c4 = shape_info.getPos()

        oldPix  = wx.Bitmap(name)
        tmp_img = oldPix.ConvertToImage()
        tmp_img.Rescale(c3, c4)
        oldPix = tmp_img.ConvertToBitmap()
        newPix  = wx.EmptyBitmap(c3, c4)
        mem = wx.MemoryDC()
        mem.SelectObject(newPix)          # because wxEmptyBitmap only
        mem.SetBackground(wx.BLACK_BRUSH)  # allocates the space
        mem.Clear()

        mem.SetPen(wx.RED_PEN)
        mem.SetBrush(wx.Brush('RED'))
        if shape == 1:
            mem.DrawRectangle(0, 0, c3, c4)
        elif shape == 2:
            mem.DrawRoundedRectangle(0, 0, c3, c4, self.rr_radius)
        elif shape == 3:
            mem.DrawEllipse(0, 0, c3, c4)
        
        mem.SelectObject(oldPix)
        newPix.SetMask(wx.Mask(newPix, wx.RED))
        mem.DrawBitmap(newPix, 0, 0, True)
        oldPix.SetMask(wx.Mask(newPix, wx.BLACK))

        return oldPix

#-------------------------------------------#
    def updateShapeList(self):
        shape_list = self.shape_list
        scale_factor = self.scale_factor

        for ind in shape_list:
            ind.scale(scale_factor)

#-------------------------------------------#
    def drawHiddenBmp(self):
        '''
        Draw all shapes to a hidden bitmap, where we assign a unique color to each
        shape. When user clicks on a shape, we use the unique color to determine
        which shape was selected.
        '''
        oldPix  = wx.EmptyBitmap(self.width, self.height)
        dc = wx.MemoryDC()
        dc.SelectObject(oldPix)
        dc.SetBackground(wx.WHITE_BRUSH)  # allocates the space
        dc.Clear()                       # The images have to be cleared

        shape_list = self.shape_list
        shape_i = 0

        dc.SetPen(wx.Pen("black",1))

        for obj in self.shape_list:

            shape = obj.shape_type
            c1, c2, c3, c4 = obj.getPos()
            c = (shape_i, 0, 0)
            shape_i += 1
            dc.SetBrush(wx.Brush(c))
            if shape == 1:
                dc.DrawRectangle(c1, c2, c3, c4)
            elif shape == 2:
                dc.DrawRoundedRectangle(c1, c2, c3, c4, self.rr_radius)
            elif shape == 3:
                dc.DrawEllipse(c1, c2, c3, c4)

        self.hidden_canvas = oldPix


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

        shape_list = self.shape_list
        for obj in self.shape_list:

            shape = obj.shape_type
            c1, c2, c3, c4 = obj.getPos()
            c = obj.color

            if obj.img:
                dc.DrawBitmap(obj.img, c1, c2, True)
            else:
                dc.SetBrush(wx.Brush(c))
                if shape == 1:
                    dc.DrawRectangle(c1, c2, c3, c4)
                elif shape == 2:
                    dc.DrawRoundedRectangle(c1, c2, c3, c4, self.rr_radius)
                elif shape == 3:
                    dc.DrawEllipse(c1, c2, c3, c4)

            if obj.text:
                dc.DrawLabel(obj.text, (c1, c2, c3, c4), wx.ALIGN_CENTER)


        dc.SetPen(wx.Pen("black",4))
        dc.DrawLineList([(0, 0, self.width, 0), 
                (self.width, 0, self.width, self.height),
                (self.width, self.height, 0, self.height),
                (0, self.height, 0, 0)]
                )
