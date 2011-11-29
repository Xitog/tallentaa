# -*- coding: utf-8 -*-

# Import
import pygame
from pygame.locals import *

# Init
pygame.init()

pygame.display.set_caption('Woolfie 3D')

resolution = (800,600)
flags = pygame.DOUBLEBUF

print(pygame.display.mode_ok(resolution))
# 0 : not ok
# !0: best color depth

screen = pygame.display.set_mode(resolution,flags,32)

sprite1 = pygame.image.load('level1.png').convert()
sprite1.set_colorkey((255,0,255))
tx, ty = sprite1.get_size()

lvl = { 'tex' : sprite1, 'h' : tx, 'w' : ty, 'lvl' : 100 }
cam = { 'x' : 0, 'y' : 0, 'h' : 800, 'w' : 600 }

def center(cam, lvl):
    cam['x'] = lvl['h'] / 2 - cam['h'] / 2
    cam['y'] = lvl['w'] / 2 - cam['w'] / 2

def blit(screen, cam, lvl):
    screen.blit(lvl['tex'], (0,0), (cam['x'],cam['y'], cam['h'],cam['w']))

clock = pygame.time.Clock()

escape = False

area = [[1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,1,0,1,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1]]

position = [212,212]    # position vector (point)
direction = [1,0]       # direction vector
camera = [0, 0.66]      # camera plane (orthogonal to direction vector) 2 * atan(0.66/1.0)=66°

modx = 0.0
mody = 0.0

# 5/11/11:1449 : OK
center(cam, lvl)
print cam['x'], cam['y']

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
            if event.key == K_LEFT or event.key == K_RIGHT:
                modx = 0
            if event.key == K_DOWN or event.key == K_UP:
                mody = 0
        if event.type == MOUSEBUTTONDOWN: # The button will be set to 4 when the wheel is rolled up, and to button 5 
            if event.button == 4:
                nx = int(lvl['w'] * 0.90)
                ny = int(lvl['h'] * 0.90)
                lvl['lvl'] = int(lvl['lvl']*0.90)
                print nx, ny, lvl['lvl']
                s = pygame.Surface((nx, ny))
                pygame.transform.smoothscale(lvl['tex'], (nx, ny), s)
                lvl['w'] = nx
                lvl['h'] = ny
                lvl['tex'] = s
                cam['x'] = int(cam['x'] * 0.90)
                cam['y'] = int(cam['y'] * 0.90)
            elif event.button == 5:
                nx = int(lvl['w'] * 1.10)
                ny = int(lvl['h'] * 1.10)
                lvl['lvl'] = int(lvl['lvl']*1.10)
                print nx, ny, lvl['lvl']
                s = pygame.Surface((nx, ny))
                pygame.transform.smoothscale(lvl['tex'], (nx, ny), s)
                lvl['w'] = nx
                lvl['h'] = ny
                lvl['tex'] = s
                cam['x'] = int(cam['x'] * 1.10)
                cam['y'] = int(cam['y'] * 1.10)
    
    # Update
    position[0] += modx
    position[1] += mody
    cam['x'] += modx
    cam['y'] += mody
    
    # Draw
    screen.fill((0,0,0))
    
    blit(screen, cam, lvl)
    #screen.blit(sprite1, (100, 100))
    
    for i in range(0, len(area)):
        line = area[i]
        for j in range(0, len(line)):
            #print(len(area))
            #print(len(line))
            #print(i,j,line[j])
            #raw_input()
            #exit()
            rx = j * 10 + 200
            ry = i * 10 + 200
            if line[j] == 1:
                color = (0,255,0)
            else:
                color = (255,255,255)
            pygame.draw.rect(screen, color, (rx,ry,10,10), 0)
    
    screen.set_at(position, (255,0,0))
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60) 
