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
    [1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1],
]

MAP_X = 10
MAP_Y = 10

#MAX_VIEW_X = 10
#MAX_VIEW_Y = 8

SCROLL_MOD = 1

while 1:
    
    mx, my = pygame.mouse.get_pos()
    mx32 = (mx-X) / 32
    my32 = (my-Y) / 32
    
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
            elif event.key == K_SPACE:
                SCROLL_MOD += 1
        elif event.type == MOUSEBUTTONDOWN:
            if mx32 in range(0, MAP_X) and my32 in range(0, MAP_Y):
                print my_map[mx32][my32]
    
    if left:
        X+=SCROLL_MOD
    if right:
        X-=SCROLL_MOD
    if down:
        Y-=SCROLL_MOD
    if up:
        Y+=SCROLL_MOD
    
    #print X, Y
    
    screen.fill(Color(0, 0, 0, 255))
    
    pygame.draw.circle(screen, Color(255, 255, 255, 255), (10+X, 10+Y), 10, 0)
    
    for yy in range(0, MAP_Y):
        for xx in range(0, MAP_X):
            #sys.stdout.write(str(my_map[yy][xx]))
            r = my_map[yy][xx]
            if r == 1:
                pygame.draw.rect(screen, Color(255, 0, 0, 128), (xx*32+X, yy*32+Y, 32, 32), 1)
            else:
                pygame.draw.rect(screen, Color(0, 255, 0, 128), (xx*32+X, yy*32+Y, 32, 32), 1)
    
    #screen.blit(ball, ballrect)
    pygame.display.flip()
    
    pygame.time.Clock().tick(60)


