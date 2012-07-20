#! /usr/bin/env python

import pygame, sys, math
from pygame.locals import *

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

MAP_X = 32
MAP_Y = 32
MAX_X = 10
MAX_Y = 10
X = 0
Y = 0

area = []
for yy in range(0, MAP_Y):
    area.append([])
    for xx in range(0, MAP_X):
        area[yy].append(0)
        sys.stdout.write(str(area[yy][xx]))
    print
area[4][4] = 1
area[31][31] = 1
area[3][2] = 1

down = False
up = False
left = False
right = False

apply = False
content = [
    ('none', 0, 0),
    ('tree1', -48, -4*32),
    ('tree2', -48, -4*32),
    ('tree3', -48, -4*32),
  ]
actual_content = 1

content_img = []
for c in content:
    i =  pygame.image.load(c[0]+'.png').convert()
    i.set_colorkey((255,0,255))
    content_img.append(i)

while 1:
    #-------------------------------------------------------------------
    # IO
    mx, my = pygame.mouse.get_pos()
    mx32 = mx / 32 + X
    my32 = my / 32 + Y
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key == K_DOWN: down = True
            elif event.key == K_UP: up = True
            elif event.key == K_LEFT: left= True
            elif event.key == K_RIGHT: right = True
        elif event.type == KEYUP:
            if event.key == K_DOWN: down = False
            elif event.key == K_UP: up = False
            elif event.key == K_LEFT: left = False
            elif event.key == K_RIGHT: right = False
            elif event.key == K_SPACE: actual_content += 1
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                apply = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                apply = False
            elif event.button == 3:
                print 'line=', my32, 'column=', mx32, Y, X
                if mx32 > 0 and mx32 < MAP_X and my32 > 0 and my32 < MAP_Y: print area[my32][mx32]
    
    #-------------------------------------------------------------------
    # Update
    if left and X > 0: X -= 1
    if right and X < MAP_X-MAX_X: X += 1
    if down and Y < MAP_Y-MAX_Y: Y += 1
    if up and Y > 0: Y -= 1
    #if left or right or down or up: print X, Y
    if apply:
        if mx32 >= 0 and mx32 < MAP_X and my32 >= 0 and my32 < MAP_Y: area[my32][mx32] = actual_content
        print 'apply=', actual_content
    
    #-------------------------------------------------------------------
    # Draw
    screen.fill(Color(0, 0, 0, 255))
    for yy in range(0, MAX_Y):
        for xx in range(0, MAX_X):
            #try:
            r = area[yy+Y][xx+X]
            #except:
            #    print 'y=', Y, yy+Y, 'x=', X, xx+X
            if r > 0:
                pygame.draw.rect(screen, Color(255, 0, 0, 128), (xx*32, yy*32, 32, 32), 1)
                screen.blit(content_img[r], (xx*32+content[r][1],yy*32+content[r][2]))
            else:
                pygame.draw.rect(screen, Color(0, 255, 0, 128), (xx*32, yy*32, 32, 32), 1)
    screen.blit(content_img[actual_content], (500, 400))
    pygame.display.flip()
    pygame.time.Clock().tick(60)
