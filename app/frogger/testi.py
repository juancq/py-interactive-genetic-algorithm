import wx
from wxPython.wx import NULL
import os, sys
import thread
pyGame=None


class SDLThread:
     def __init__(self,screen):
          self.m_bKeepGoing=self.m_bRunning=False
          self.screen=screen
          self.color=(255,0,0)
          self.rect=(10,10,100,100)

     def Start(self):
          self.m_bKeepGoing = self.m_bRunning = True
          thread.start_new_thread(self.Run, ())

     def Stop(self):
          self.m_bKeepGoing = False

     def IsRunning(self):
          return self.m_bRunning

     def Run(self):
        while self.m_bKeepGoing:
             e=pyGame.event.poll()
             if e.type==pyGame.MOUSEBUTTONDOWN:
                  self.color=(255,0,128)
                  self.rect=(e.pos[0],e.pos[1],100,100)
                  print e.pos
             self.screen.fill((0,0,0))
             self.screen.fill(self.color,self.rect)
             pyGame.display.flip()
        self.m_bRunning=False;

class SDLPanel(wx.Panel):
    def __init__(self,parent,ID,tplSize):
        global pyGame
        wx.Panel.__init__(self,parent,ID,size=tplSize)
        self.Fit()
        os.environ['SDL_WINDOWID']=str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame
        pyGame=pygame
        pyGame.display.init()
        window = pyGame.display.set_mode(tplSize)
        self.thread=SDLThread(window)
        self.thread.Start()

class MyFrame(wx.Frame):
    def __init__(self,parent,ID,strTitle,tplSize):
        wx.Frame.__init__(self,parent,ID,strTitle,size=tplSize)
        self.pnlSDL=SDLPanel(self,-1,tplSize)
        #self.Fit()

app = wx.PySimpleApp()
frame = MyFrame(NULL, -1, 'SDL Frame',(640,480))
frame.Show()
app.MainLoop()

