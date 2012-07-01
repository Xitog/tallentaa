#! /usr/bin/env python

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X et Y / 32 -> donne le carre ou on est.
# remultiplie par 32 -> donne la ou on commence a afficher

import pygame, sys
from pygame.locals import *

pygame.init()

size = width, height = 320, 240

screen = pygame.display.set_mode(size)

X = 0
Y = 0

left = False
right = False
up = False
down = False

view_left_up = (0,0)

my_map = [
    [1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key == K_DOWN:
                down = True
            elif event.key == K_UP:
                up = True
            elif event.key == K_LEFT:
                left= True
            elif event.key == K_RIGHT:
                right = True
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                down = False
            elif event.key == K_UP:
                up = False
            elif event.key == K_LEFT:
                left = False
            elif event.key == K_RIGHT:
                right = False
    
    if left:
        X+=1
    if right:
        X-=1
    if down:
        Y-=1
    if up:
        Y+=1
    
    #print X, Y
    
    screen.fill(Color(0, 0, 0, 255))
    
    pygame.draw.circle(screen, Color(255, 255, 255, 255), (10+X, 10+Y), 10, 0)
    
    view_left_up = (X%32,Y%32)
    
    MAX_VIEW_X = 9
    MAX_VIEW_Y = 7
    
    for yy in range(0, MAX_VIEW_Y):
        for xx in range(0, MAX_VIEW_X):
            #sys.stdout.write(str(my_map[yy][xx]))
            r = my_map[yy][xx]
            if r == 1:
                pygame.draw.rect(screen, Color(255, 0, 0, 128), (xx*32, yy*32, 32, 32), 1)
            else:
                pygame.draw.rect(screen, Color(0, 255, 0, 128), (xx*32, yy*32, 32, 32), 1)
        #print
    #raw_input()
    
    #screen.blit(ball, ballrect)
    pygame.display.flip()
    
    pygame.time.Clock().tick(60)


