import wx

class Test(wx.App):
    def OnInit(self):
        oldPix  = wx.EmptyBitmap(300, 300)
        newPix  = wx.EmptyBitmap(300, 300)

        mem = wx.MemoryDC()
        mem.SelectObject(oldPix)
        mem.Clear()                       # The images have to be cleared
        mem.SelectObject(newPix)          # because wxEmptyBitmap only
        mem.SetBackground(wx.BLACK_BRUSH)  # allocates the space
        mem.Clear()

        # We now have a black and a white image
        # Next we plot a white box in the middle of the black image
        
        mem.SetPen(wx.RED_PEN)
        mem.SetBrush(wx.Brush('RED'))
        #mem.DrawLines(((100, 200), (100, 100), (200, 100), (200,200), (100,200)))
        mem.DrawEllipse(100, 100, 90, 110)#, 0, 360)
        
        mem.SelectObject(oldPix)
        newPix.SetMask(wx.Mask(newPix, wx.BLACK))
        mem.DrawBitmap(newPix, 0, 0, 1)
        oldPix.SetMask(wx.Mask(newPix, wx.BLACK))

        #oldPix.SaveFile("oldPix.bmp", wx.BITMAP_TYPE_BMP)
        oldPix.SaveFile("oldPix.png", wx.BITMAP_TYPE_PNG)
        newPix.SaveFile("newPix.bmp", wx.BITMAP_TYPE_BMP)
        return True

        
app = Test(0)
app.MainLoop()

