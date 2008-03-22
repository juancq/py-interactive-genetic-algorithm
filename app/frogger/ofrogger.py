#!/usr/bin/python

import pygame
from pygame.locals import *
import time
import os

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# Load background
board = pygame.image.load('background.png').convert()

# Load frog
frog = pygame.image.load('frog.tga').convert()
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
