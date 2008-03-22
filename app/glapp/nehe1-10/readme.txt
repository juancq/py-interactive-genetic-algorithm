Pygame + PyOpenGL version of Nehe's OpenGL lessons
Paul Furber 2001 - m@verick.co.za

Pygame   : http://www.pygame.org
PyOpenGL : http://pyopengl.sf.net
NEHE     : http://nehe.gamedev.net


The NEHE Opengl tutorials are a set if simple tutorials
that gradually ramp the user up to different parts of
OpenGL development. Starting with opening a window, and
moving up to things like particle systems and transparent
textures.

The original tutorials are written in C with OpenGL and
the GLUT library. Since then they have been ported to
many different languages and libraries. These tutorials
have been converted to python using PyOpenGL and Pygame.
They are generally straight conversions of the C code,
not a real rewrite into python.

Due to some crossplatform resizing issues with mixing
pygame and pyopengl, the created windows do not resize.


Finally, here are some quick notes from Paul Furber.

    Although nearly all of it is a direct translation
    from the Linux+SDL C conversion there's some code
    that was to tempting not to do in a more pythonesque
    way :) example09 - the star class and example 10 -
    the filereading and data structure. 

