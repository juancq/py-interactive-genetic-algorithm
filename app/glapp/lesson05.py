#!/usr/bin/env python
# pygame + PyOpenGL version of Nehe's OpenGL lesson05
# Paul Furber 2001 - m@verick.co.za

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

rtri = rquad = 0.0

def resize((width, height)):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def draw():
    global rtri, rquad

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
    glLoadIdentity();					
    glTranslatef(-1.5,0.0,-6.0)

    glRotatef(rtri,0.0,1.0,0.0)			

    glBegin(GL_TRIANGLES)				

    glColor3f(1.0,0.0,0.0)
    glVertex3f( 0.0, 1.0, 0.0)		
    glColor3f(0.0,1.0,0.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f( 1.0,-1.0, 1.0)
    
    glColor3f(1.0,0.0,0.0)	
    glVertex3f( 0.0, 1.0, 0.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f( 1.0,-1.0, 1.0)
    glColor3f(0.0,1.0,0.0)	
    glVertex3f( 1.0,-1.0, -1.0)

    glColor3f(1.0,0.0,0.0)	
    glVertex3f( 0.0, 1.0, 0.0)
    glColor3f(0.0,1.0,0.0)	
    glVertex3f( 1.0,-1.0, -1.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0,-1.0, -1.0)
		
		
    glColor3f(1.0,0.0,0.0)	
    glVertex3f( 0.0, 1.0, 0.0)
    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0,-1.0,-1.0)
    glColor3f(0.0,1.0,0.0)	
    glVertex3f(-1.0,-1.0, 1.0)
    glEnd()


    glLoadIdentity()
    glTranslatef(1.5,0.0,-7.0)
    glRotatef(rquad,1.0,1.0,1.0)
    glBegin(GL_QUADS)	


    glColor3f(0.0,1.0,0.0)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)		
    glVertex3f(-1.0, 1.0, 1.0)		
    glVertex3f( 1.0, 1.0, 1.0)		

    glColor3f(1.0,0.5,0.0)	
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)		
    glVertex3f(-1.0,-1.0,-1.0)		
    glVertex3f( 1.0,-1.0,-1.0)		

    glColor3f(1.0,0.0,0.0)		
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)		
    glVertex3f(-1.0,-1.0, 1.0)		
    glVertex3f( 1.0,-1.0, 1.0)		

    glColor3f(1.0,1.0,0.0)	
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)		
    glVertex3f( 1.0, 1.0,-1.0)		

    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)		
    glVertex3f(-1.0,-1.0,-1.0)		
    glVertex3f(-1.0,-1.0, 1.0)		

    glColor3f(1.0,0.0,1.0)	
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)		
    glVertex3f( 1.0,-1.0,-1.0)		
    glEnd()	

    rtri  = rtri + 0.2                  
    rquad = rquad - 0.15                
    

def main():

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode((640,480), video_flags)

    resize((640,480))
    init()

    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        elif event.type == KEYDOWN and event.key == K_a:
            resize((800,600))

        draw()
        pygame.display.flip()
        frames = frames+1

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))


if __name__ == '__main__': main()

