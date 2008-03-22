#!/usr/bin/env python
# pygame + PyOpenGL version of Nehe's OpenGL lesson09
# Paul Furber 2001 - m@verick.co.za

import os, random
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, pygame.image, pygame.key
from pygame.locals import *


textures = []
stars = []
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
        global zoom, tilt, twinkle, stars
        glLoadIdentity( )
        glTranslatef( 0.0, 0.0, zoom )
        glRotatef( tilt, 1.0, 0.0, 0.0 )
        glRotatef( self.angle, 0.0, 1.0, 0.0 )
        glTranslatef( self.dist, 0.0, 0.0 )
        glRotatef( -self.angle, 0.0, 1.0, 0.0 )
        glRotatef( -tilt, 1.0, 0.0, 0.0 )
        if twinkle:
            self.r = stars[self.max - self.index - 1].r
            self.g = stars[self.max - self.index - 1].g
            self.b = stars[self.max - self.index - 1].b
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
    global stars
    
    glEnable(GL_TEXTURE_2D)
    load_textures()
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glBlendFunc( GL_SRC_ALPHA, GL_ONE )
    glEnable(GL_BLEND)
    for x in range(50):
        stars.append(star(x))

def load_textures():
    global textures
    
    texturefile = os.path.join('data','star.bmp')
    textureSurface = pygame.image.load(texturefile)
    textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

    textures = glGenTextures(2)
    
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    
def draw():
    global stars
    
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glBindTexture( GL_TEXTURE_2D, textures[0] )
    glLoadIdentity( );
    for x in range(50):
        stars[x].update()


def handle_keys(key):
    global tilt, zoom, twinkle
    
    if key==K_ESCAPE:
        return 0

    if key==K_UP:
        tilt += 2.0
    elif key==K_DOWN:
        tilt -= 2.0
    elif key==K_PAGEUP:
        zoom += 0.5
    elif key==K_PAGEDOWN:
        zoom -=0.5
    elif key==K_t:
        twinkle = not twinkle

    return 1

def main():

    global surface

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    surface = pygame.display.set_mode((640,480), video_flags)
    pygame.key.set_repeat(100,30)

    random.seed()
    resize((640,480))
    init()

    frames = 0
    done = 0
    ticks = pygame.time.get_ticks()
    while not done:
        while 1:
            event = pygame.event.poll()
            if event.type == NOEVENT:
                break
            if event.type == KEYDOWN:
                if handle_keys(event.key) == 0:
                    done = 1
            if event.type == QUIT:
                done = 1
        
        draw()
        pygame.display.flip()
        frames += 1


    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))


if __name__ == '__main__': main()
