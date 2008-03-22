from wx.glcanvas import GLCanvas
import wx
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

name = 'ball_glut'

class myGLCanvas(GLCanvas):
    def __init__(self, parent, color = [1.0,0.,0.,1.]):
	GLCanvas.__init__(self, parent,-1)
	wx.EVT_PAINT(self, self.OnPaint)
	self.init = 0
        self.color = color
        wx.EVT_CHAR(self, self.OnKey)

        self.Bind(wx.EVT_SIZE, self.processSizeEvent, self)


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

    def OnReshape(self, width, height):
        """Reshape the OpenGL viewport based on the dimensions of the window."""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, float(width)/height, 0.1, 30.0)

    
    def GetGLExtents(self):
        """Get the extents of the OpenGL canvas."""
        return self.GetClientSize()

    def processSizeEvent(self, event):
        """Process the resize event.""" 
        if self.GetContext():
            # Make sure the frame is shown before calling SetCurrent.
            self.Show()
            self.SetCurrent()
            
            size = self.GetGLExtents()
            self.OnReshape(size.width, size.height)
            self.Refresh(False)
        event.Skip()


    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
	glMaterialfv(GL_FRONT,GL_DIFFUSE,self.color)
        glBegin(GL_TRIANGLES)
        glVertex( 1.0, 0.0, 0.0 )
        glVertex( 0.0, 1.0, 0.0 )
        glVertex( -1.0, 0.0, 0.0 )
        glEnd()
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
