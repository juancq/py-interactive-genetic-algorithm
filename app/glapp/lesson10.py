#!/usr/bin/env python
# pygame + PyOpenGL version of Nehe's OpenGL lesson10
# Paul Furber 2001 - m@verick.co.za

import os, random
from string import split
from math import sin, cos
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, pygame.image, pygame.key
from pygame.locals import *


textures = []
filter = 0
tris = []

yrot = 0.0
xpos = 0.0
zpos = 0.0

lookupdown = 0.0
walkbias = 0.0
walkbiasangle = 0.0

LightAmbient  = [ 0.5, 0.5, 0.5, 1.0]
LightDiffuse  = [ 1.0, 1.0, 1.0, 1.0]
LightPosition = [ 0.0, 0.0, 2.0, 1.0]

piover180 = 0.0174532925

def resize((width, height)):
    if height==0:
        height=1.0
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(width)/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    global lookupdown, walkbias, walkbiasangle
    
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
    lookupdown    = 0.0
    walkbias      = 0.0
    walkbiasangle = 0.0
    glColor4f( 1.0, 1.0, 1.0, 0.5)


def load_textures():
    global textures
    
    texturefile = os.path.join('data','mud.bmp')
    textureSurface = pygame.image.load(texturefile)
    textureData = pygame.image.tostring(textureSurface, "RGBX", 1)

    textures = glGenTextures(3)
    
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, textureData )
    gluBuild2DMipmaps( GL_TEXTURE_2D, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(),
                       GL_RGBA, GL_UNSIGNED_BYTE, textureData );

def setup_world():
    global tris
    verts = 0
    tri = []
    
    f = open(os.path.join("data", "world.txt"))
    lines = f.readlines()
    f.close()
    for line in lines:
        vals = split(line)
        if len(vals) != 5:
            continue
        if vals[0] == '//':
            continue
        
        vertex = []
        for val in vals:
            vertex.append(float(val))
        tri.append(vertex)
        verts += 1
        if (verts == 3):
            tris.append(tri)
            tri = []
            verts = 0

def draw():
    global xpos, zpos, yrot, walkbias, lookupdown
    global textures, filter, tris

    xtrans = -xpos
    ztrans = -zpos
    ytrans = -walkbias-0.25
    sceneroty=360.0-yrot

    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glRotatef( lookupdown, 1.0, 0.0 , 0.0 )
    glRotatef( sceneroty, 0.0, 1.0 , 0.0 )
    glTranslatef( xtrans, ytrans, ztrans )
    glBindTexture( GL_TEXTURE_2D, textures[filter] )

    for tri in tris:
        glBegin(GL_TRIANGLES)
        glNormal3f( 0.0, 0.0, 1.0)
        
        glTexCoord2f(tri[0][3], tri[0][4])
        glVertex3f(tri[0][0], tri[0][1], tri[0][2])

        glTexCoord2f(tri[1][3], tri[1][4])
        glVertex3f(tri[1][0], tri[1][1], tri[1][2])

        glTexCoord2f(tri[2][3], tri[2][4])
        glVertex3f(tri[2][0], tri[2][1], tri[2][2])

        glEnd()

def handle_keys(key):
    global xpos, zpos, yrot, filter
    global piover180, walkbiasangle, walkbias
    
    if key==K_ESCAPE:
        return 0

    if key==K_f:
        filter +=1
        if filter == 3:
            filter = 0
    if key==K_RIGHT:
        yrot -= 1.5
    if key==K_LEFT:
        yrot += 1.5
    if key==K_UP:
        xpos -= sin( yrot * piover180 ) * 0.05
        zpos -= cos( yrot * piover180 ) * 0.05
        if ( walkbiasangle >= 359.0 ):
            walkbiasangle = 0.0
        else:
            walkbiasangle += 10.0
        walkbias = sin( walkbiasangle * piover180 ) / 20.0
    if key==K_DOWN:
        xpos += sin( yrot * piover180 ) * 0.05
        zpos += cos( yrot * piover180 ) * 0.05
        if ( walkbiasangle <= 1.0 ):
            walkbiasangle = 359.0
        else:
            walkbiasangle -= 10.0
        walkbias = sin( walkbiasangle * piover180 ) / 20.0

    return 1

def main():

    global surface

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    surface = pygame.display.set_mode((640,480), video_flags)
    pygame.key.set_repeat(100,0)

    random.seed()
    resize((640,480))
    init()
    setup_world()

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
