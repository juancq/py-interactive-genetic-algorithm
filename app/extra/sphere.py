from wx.glcanvas import GLCanvas
import wx
#from wx import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys,math

name = 'ball_glut'

class myGLCanvas(GLCanvas):
    def __init__(self, parent, color = [1.0,0.,0.,1.]):
	GLCanvas.__init__(self, parent,-1)
	wx.EVT_PAINT(self, self.OnPaint)
	self.init = 0
        self.color = color
        wx.EVT_CHAR(self, self.OnKey)
	return

    def OnKey(self, event):
        keycode = chr(event.GetKeyCode())
        if keycode == 'j':
            print 'a was pressed'

    def OnPaint(self,event):
	dc = wx.PaintDC(self)
	self.SetCurrent()
	if not self.init:
	    self.InitGL()
	    self.init = 1
	self.OnDraw()
	return

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
	glMaterialfv(GL_FRONT,GL_DIFFUSE,self.color)
	glutSolidSphere(8,40,80)
	glPopMatrix()
        self.SwapBuffers()
        return
	
    def InitGL(self):
        # set viewing projection
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_position = [1.0, 1.0, 1.0, 0.0]

        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 10.0,
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)
        return


class M(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        glutInit(' ')
        ball1 = myGLCanvas(self, color = [0.0,0.0,1.0,0.0])
        ball2 = myGLCanvas(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(ball1, 1, wx.EXPAND)
        sizer.Add(ball2, 1, wx.EXPAND)
        self.SetSizer(sizer)
    

def main():
    app = wx.PySimpleApp()
    frame = wx.Frame(None,-1,'ball_wx', wx.DefaultPosition, wx.Size(400,400))
    #canvas = myGLCanvas(frame)
    panel = M(frame)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__': main()
