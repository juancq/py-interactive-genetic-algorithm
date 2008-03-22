#!/usr/bin/env python
# pygame + PyOpenGL version of Nehe's OpenGL lesson08
# Paul Furber 2001 - m@verick.co.za

import os
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, pygame.image
from pygame.locals import *


xrot = yrot = 0.0
xspeed = yspeed = 0.0
z = -5.0
textures = []
filter = 0
light = 0
blend = 0

LightAmbient  = ( (0.5, 0.5, 0.5, 1.0) );
LightDiffuse  = ( (1.0, 1.0, 1.0, 1.0) );
LightPosition = ( (0.0, 0.0, 2.0, 1.0) );


def resize((width, height)):
    if height==0:
        height=1.0
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glEnable(GL_TEXTURE_2D)
    load_textures()
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glLightfv( GL_LIGHT1, GL_AMBIENT, LightAmbient )
    glLightfv( GL_LIGHT1, GL_DIFFUSE, LightDiffuse )
    glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )
    glEnable( GL_LIGHT1 )
    glColor4f( 1.0, 1.0, 1.0, 0.5)
    glBlendFunc( GL_SRC_ALPHA, GL_ONE )


def load_textures():
    global LightAmbient, LightDiffuse, LightPosition, textures
    
    texturefile = os.path.join('data','glass.bmp')
    textureSurface = pygame.image.load(texturefile)
    textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

    textures = glGenTextures(3)
    
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, textures[1])
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )

    glBindTexture( GL_TEXTURE_2D, textures[2])
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    gluBuild2DMipmaps( GL_TEXTURE_2D, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(),
                       GL_RGBA, GL_UNSIGNED_BYTE, textureData);



def draw():
    global xrot, yrot, xspeed, yspeed, z, filter
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, z)

    glRotatef(xrot, 1.0, 0.0, 0.0)
    glRotatef(yrot, 0.0, 1.0, 0.0)

    glBindTexture(GL_TEXTURE_2D, textures[filter])
    
    glBegin(GL_QUADS)
	
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
	
    # Back Face
    glNormal3f(0.0, 0.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
	
    # Top Face
    glNormal3f(0.0, 1.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	
    # Bottom Face
    glNormal3f(0.0, -1.0, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	
    # Right face
    glNormal3f(1.0, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	
    # Left Face
    glNormal3f(-1.0, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	
    glEnd();				
    
    xrot += xspeed
    yrot += yspeed

def handle_keys(key):
    global filter, light, z, xspeed, yspeed, blend

    if key == K_ESCAPE:
        return 0
    if key == K_f:
        filter = filter + 1
        if filter == 3:
            filter = 0
    elif key == K_l:
        light = not light
        if not light:
            glDisable(GL_LIGHTING)
        else:
            glEnable(GL_LIGHTING)
    elif key == K_b:
        blend = not blend
        if blend:
            glEnable(GL_BLEND)
            glDisable(GL_DEPTH_TEST)
        else:
            glEnable(GL_DEPTH_TEST)
            glDisable(GL_BLEND)
    elif key == K_PAGEUP:
        z -= 0.05
    elif key == K_PAGEDOWN:
        z += 0.05
    elif key == K_UP:
        xspeed -= 0.01
    elif key == K_DOWN:
        xspeed += 0.01
    elif key == K_LEFT:
        yspeed -= 0.01
    elif key == K_RIGHT:
        yspeed += 0.01
    
    return 1

def main():

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    surface = pygame.display.set_mode((640,480), video_flags)

    resize((640,480))
    init()

    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT:
            break
        if event.type == KEYDOWN:
            if handle_keys(event.key) == 0:
                break
        
        draw()
        pygame.display.flip()
        frames = frames+1

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))


if __name__ == '__main__': main()
