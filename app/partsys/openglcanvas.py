from wx.glcanvas import GLCanvas
import wx
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random
import pygame

init = 0
twinkle = 0
zoom = -15.0
tilt = 90.0
spin = 0.0


class star:
    """ simple star class that (hopefully) demonstrates
    how to move functionality out of a main loop and into
    an object - the logic remains unchanged from the
    original tutorial C code"""
    def __init__(self, index, max=50):
        self.angle = 0.0
        self.index = index
        self.max = max
        self.dist = (1.0 * index/max) * 5.0
        self.r = random.randrange(0,256)
        self.g = random.randrange(0,256)
        self.b = random.randrange(0,256)

    def init(self, stars):
        self.stars = stars

    def draw(self):
        glBegin( GL_QUADS )
        glTexCoord2f( 0.0, 0.0 ); glVertex3f( -1.0, -1.0, 0.0 )
        glTexCoord2f( 1.0, 0.0 ); glVertex3f(  1.0, -1.0, 0.0 )
        glTexCoord2f( 1.0, 1.0 ); glVertex3f(  1.0,  1.0, 0.0 )
        glTexCoord2f( 0.0, 1.0 ); glVertex3f( -1.0,  1.0, 0.0 )
        glEnd( )

    def set_color(self):
        glColor4ub(self.r, self.g, self.b, 255)

    def orient(self):
        global zoom, tilt, twinkle
        glLoadIdentity( )
        glTranslatef( 0.0, 0.0, zoom )
        glRotatef( tilt, 1.0, 0.0, 0.0 )
        glRotatef( self.angle, 0.0, 1.0, 0.0 )
        glTranslatef( self.dist, 0.0, 0.0 )
        glRotatef( -self.angle, 0.0, 1.0, 0.0 )
        glRotatef( -tilt, 1.0, 0.0, 0.0 )
        if twinkle:
            self.r = self.stars[self.max - self.index - 1].r
            self.g = self.stars[self.max - self.index - 1].g
            self.b = self.stars[self.max - self.index - 1].b
            self.set_color()
            self.draw()
        glRotatef( spin, 0.0, 0.0, 1.0 )
 
    def update(self):
        global spin
        self.orient()
        self.set_color()
        self.draw()
        spin += 0.01
        self.angle += 1.0*self.index / self.max
        self.dist -= 0.01
        if ( self.dist < 0.0 ):
            self.dist += 5.0
            self.r = random.randrange(0,256)
            self.g = random.randrange(0,256)
            self.b = random.randrange(0,256)

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


        self.stars = [star(x) for x in xrange(50)]
        for s in self.stars: s.init(self.stars)
        self.textures = self.load_textures()

        TIMER_ID = wx.NewId()
        self.timer = wx.Timer(self, TIMER_ID)  # message will be sent to the panel
        # milliseconds
        self.timer.Start(tick)
        wx.EVT_TIMER(self, TIMER_ID, self.tick)  # call the on_timer function

    def load_textures(self):
        textures = []
        
        texturefile = os.path.join('data','star.bmp')
        print 'texturefile ', texturefile
        print os.getcwd()
        textureSurface = pygame.image.load('app/partsys/'+texturefile)
        textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

        textures = glGenTextures(2)
        
        glBindTexture(GL_TEXTURE_2D, textures[0])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                      GL_RGBA, GL_UNSIGNED_BYTE, textureData )
        return textures

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
        #gluLookAt(5., 0., 5., 0., 0., 0., 0., 1., 0.)

        if height==0:
            height=1.0
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.1, 100.0)
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

        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glBindTexture( GL_TEXTURE_2D, self.textures[0] )
        glLoadIdentity( );
        for star in self.stars:
            star.update()

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
            glEnable(GL_TEXTURE_2D)
            glShadeModel(GL_SMOOTH)
            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClearDepth(1.0)
            glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
            glBlendFunc( GL_SRC_ALPHA, GL_ONE )
            glEnable(GL_BLEND)

#------------------------------------------#
