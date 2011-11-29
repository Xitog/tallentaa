# -*- coding: utf-8 -*-

# Import
import pygame
from pygame.locals import *

# Init
pygame.init()

pygame.display.set_caption('STR')

resolution = (800,600)
flags = pygame.DOUBLEBUF

print(pygame.display.mode_ok(resolution))
# 0 : not ok
# !0: best color depth

screen = pygame.display.set_mode(resolution,flags,32)

escape = False

clock = pygame.time.Clock()

level = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

maxi = 16
maxj = 16
zoom = [4, 8, 16, 32, 64]
z    = 3
camx = 0
camy = 0
modx = 0
mody = 0

# Main loop
while not escape:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            escape = True
        if event.type == KEYDOWN and event.key == K_LEFT:
            modx = -1
        if event.type == KEYDOWN and event.key == K_RIGHT:
            modx = 1
        if event.type == KEYDOWN and event.key == K_UP:
            mody = -1
        if event.type == KEYDOWN and event.key == K_DOWN:
            mody = 1
        if event.type == KEYUP:
            modx = 0
            mody = 0
        if event.type == MOUSEBUTTONDOWN:
            print event.button
            if event.button == 4:
                z += 1
                z %= 5
                camx /= 2
                camy /= 2
            elif event.button == 5:
                z -= 1
                z %= 5
                camx *= 2
                camy *= 2
            print camx, camy, z, zoom[z]
    camx -= modx
    camy -= mody
    # Update
    # Draw
    screen.fill((0,0,0))
    for i in range(0, maxi):
        for j in range(0, maxj):
            pygame.draw.rect(screen, (255,0,0), (i*zoom[z]+camx, j*zoom[z]+camy, zoom[z], zoom[z]), 1)

    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60)
