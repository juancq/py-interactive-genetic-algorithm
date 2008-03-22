import froggersrc
from gui import feedbackpanel
import os

class GamePanel(feedbackpanel.FeedbackPanel):
    def __init__(self, parent, id):
        feedbackpanel.FeedbackPanel.__init__(self, parent, id, size = (350, 200))

        import sys
        ##Note we call the GetHandle() method of a control in the window/frame, not the wxFrame itself
        self.hwnd = self.GetChildren()[0].GetHandle()
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd) #must be before init

        ## NOTE WE DON'T IMPORT PYGAME UNTIL NOW.  Don't put "import pygame" at the top of the file.
        import pygame
        pygame.display.init()
        from pygame.locals import *
        #froggersrc()

        path = os.getcwd()
        pygame.init()

        size = width, height = 640, 480
        screen = pygame.display.set_mode(size)

        # Load background
        board = pygame.image.load(path+'/app/frogger/background.png').convert()

        # Load frog
        frog = pygame.image.load(path+'/app/frogger/frog.tga').convert()
        base_rect = frog.get_rect()
        frog_rect = base_rect.move(0,0)

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_UP:
                        frog_rect = frog_rect.move(0, -40)
                    elif event.key == K_DOWN:
                        frog_rect = frog_rect.move(0, 40)
                    elif event.key == K_LEFT:
                        frog_rect = frog_rect.move(-40, 0)
                    elif event.key == K_RIGHT:
                        frog_rect = frog_rect.move(40, 0)
                        

            screen.blit(board, board.get_rect())
            screen.blit(frog, frog_rect)
            pygame.display.flip()


        pygame.quit()

