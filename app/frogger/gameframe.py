import wx
import os, sys
import pygame, pygame.sprite, pygame.transform, pygame.image
from pygame.locals import *
import ofrogger

Objectimage = os.path.join('data', 'Adenine.gif')

class MyPan(wx.Panel):
    def __init__(self, parent, ID, title):
        wx.Panel.__init__(self, parent, ID,
                title, wx.DefaultPosition, wx.Size(350, 200))
        ofrogger()

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, size = (800,800))
        p1 = MyPan(self, ID, title)
        p2 = MyPan(self, ID, title)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(p1)
        sizer.AddSpacer((20, 20))
        sizer.Add(p2)
        self.SetSizer(sizer)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(NULL, -10,"BasicWinTool")
        frame.Show(true)
        self.SetTopWindow(frame)
        #
        #ofrogger()
        #
        return true
app = MyApp(0)
