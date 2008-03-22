from wx.glcanvas import GLCanvas
import wx
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
init = 0

class IGAGLCanvas(GLCanvas):
    def __init__(self, parent, data, tick = 100, size = (250, 250)):
	GLCanvas.__init__(self, parent, size = size, 
                style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
	wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_CHAR(self, self.OnKey)

        self.Bind(wx.EVT_SIZE, self.processSizeEvent, self)
        self.data = data

        self.InitGL()

        self.z = 0.0
        self.xspeed = 0.0
        self.yspeed = 0.0
        self.xrot = 0.0
        self.yrot = 0.0

        TIMER_ID = wx.NewId()
        self.timer = wx.Timer(self, TIMER_ID)  # message will be sent to the panel
        # milliseconds
        self.timer.Start(tick)
        wx.EVT_TIMER(self, TIMER_ID, self.tick)  # call the on_timer function

#------------------------------------------#
    def Destroy(self):
        self.timer.Stop()
        GLCanvas.Destroy(self)

#------------------------------------------#
    def tick(self, event):
        self.Refresh()

#------------------------------------------#
    def OnKey(self, event):
        keycode = chr(event.GetKeyCode())
        if keycode == 'j':
            self.z -= .05
        elif keycode == 'k':
            self.z += .05
        elif keycode == 'h':
            self.xspeed -= 0.2
        elif keycode == 'l':
            self.xspeed -= 0.2
        elif keycode == 'u':
            self.yspeed -= 0.2
        elif keycode == 'i':
            self.yspeed -= 0.2
        elif keycode == 's':
            self.z = 0.0
            self.xspeed = 0.0
            self.yspeed = 0.0
            self.xrot = 0.0
            self.yrot = 0.0

        event.Skip()

#------------------------------------------#
    def OnPaint(self,event):
	self.SetCurrent()
	self.OnDraw()


#------------------------------------------#
    def OnReshape(self, width, height):
        """
        Reshape the OpenGL viewport based on the dimensions of the window.
        """
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.1, 100.0)
        gluLookAt(5., 0., 5., 0., 0., 0., 0., 1., 0.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    
#------------------------------------------#
    def GetGLExtents(self):
        """Get the extents of the OpenGL canvas."""
        return self.GetClientSize()

#------------------------------------------#
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

#------------------------------------------#
    def OnDraw(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glLoadIdentity()
        glTranslatef(0.0, 0.0, self.z)
        glRotatef(self.xrot, 1.0, 0.0, 0.0)
        glRotatef(self.yrot, 0.0, 1.0, 0.0)

        v = self.data.values()

        glBegin(GL_POLYGON)				
        colors = [ (1.0,0.0,0.0),
                    (0.0,1.0,0.0),
                    (0.0,0.0,1.0) ]
        len_col = len(colors)


        j = 0
        for i in xrange(0, len(v), 3):
            r,g,b = colors[(i+j)%len_col]
            glColor3f(r, g, b)
            glVertex3f( v[i], v[i+1], v[i+2] )
            j += 1

        glEnd()

        glFinish()
        self.SwapBuffers()

        self.xrot += self.xspeed
        self.yrot += self.yspeed
	
#------------------------------------------#
    def InitGL(self):
        global init
	if not init:
	    init = 1

            glutInit('')
            glShadeModel(GL_SMOOTH)
            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClearDepth(1.0)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

#------------------------------------------#
