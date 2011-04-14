# -*- coding: utf-8 -*-
# Dig!

# Import
import pygame
from pygame.locals import *

# Init
pygame.init()
pygame.display.set_caption('Dig Edit')

MAXX = 800
MAXY = 600
resolution = (MAXX,MAXY)
flags = pygame.DOUBLEBUF
screen = pygame.display.set_mode(resolution,flags,32)

escape = False
clock = pygame.time.Clock()

v = 1
n = 32
s = 32
lvl = [[v]*n for x in xrange(n)]
alt = [[0]*n for x in xrange(n)]

act = False

item = 'Water'
mode = 'Texture'

textures = {
    'Grass' : '1_Basic.png',
    'Water' : '2_Basic2.png'
}

doodads = {
    'Desert Tree 1' : '101_DesertTree1.png',
    'Desert Tree 2' : '102_DesertTree2.png',
    'Desert Tree 3' : '103_DesertTree3.png'
}

specials = {
    'HG' : '111_HG.png',
    'HM' : '112_HM.png',
    'HD' : '113_HD.png',
    'MD' : '114_MD.png',
    'BD' : '115_BD.png',
    'BM' : '116_BM.png',
    'BG' : '117_BG.png',
    'MG' : '118_MG.png'
}

modes = {'Texture':textures, 'Doodad':doodads, 'Object': {}, 'Specials' : specials}

class Texture:
    def __init__(self, filename, alpha=255):
        try:
            elements = filename.rstrip('.png').split('_')
            self.id = int(elements[0])
            elements = elements[1:]
            self.name = ' '.join(elements)
            self.surf = pygame.image.load(filename).convert()
            self.surf.set_colorkey((255,0,255))
            self.surf.set_alpha(alpha)
            self.x = self.surf.get_size()[0]
            self.y = self.surf.get_size()[1]
            print 'Loaded ressource %s @%s as %s %dx%d' % (filename,self.id, self.name, self.x, self.y)
        except pygame.error as e:
            print 'Load error %s : %s' % (filename, str(e))

selector = Texture('0_Selector.png', 192)

quick = {}

for k in modes:
    print '----> Loading %s' % (k,)
    for i in modes[k]:
        t = Texture(modes[k][i])
        modes[k][i] = t
        quick[t.id] = t.surf

print mode
print item

import sys

pygame.mouse.set_pos([400,300])

cam_x = 0
cam_y = 0
pres = 10

activated = False

# Main loop
while not escape:
    
    m = pygame.mouse.get_pos()
    mx = m[0]
    my = m[1]
    mxg = (m[0]-cam_x)/s
    myg = (m[1]-cam_y)/s
    if mxg < 0: mxg = 0
    elif mxg > 31: mxg = 31
    if myg < 0: myg = 0
    elif myg > 31 : myg = 31

    if activated:    
        if mx < pres:
            cam_x += 1
        elif mx > MAXX-pres:
            cam_x -= 1
        if my < pres:
            cam_y += 1
        elif my > MAXY-pres:
            cam_y -= 1
    
    #print 'MX:',m[0],'MY:',m[1],'GridX:',mxg,'GridY:',myg, 'CamX:',cam_x, 'CamY:',cam_y
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        if event.type == MOUSEMOTION:
            activated = True
        if event.type == MOUSEBUTTONDOWN:
            #print event.button
            if event.button == 1:
                act = True
            elif event.button == 2:
                pass
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                act = False
            elif event.button == 2:
                for i in range(0, n):
                    for j in range(0, n):
                        sys.stdout.write(str(lvl[i][j]))
                    print
            elif event.button == 3:
                print item
                if item == 'Grass': item = 'Water'
                else: item = 'Grass'
                print item

        if act:
            if lvl[myg-1][mxg-1] == 1: lvl[myg-1][mxg-1] = 111
            else: lvl[myg-1][mxg-1] = 2
            if lvl[myg-1][mxg] == 1: lvl[myg-1][mxg] = 112
            else: lvl[myg-1][mxg] = 2
            if lvl[myg-1][mxg+1] == 1: lvl[myg-1][mxg+1] = 113
            else: lvl[myg-1][mxg+1] = 2
            if lvl[myg][mxg+1] == 1: lvl[myg][mxg+1] = 114
            else: lvl[myg][mxg+1] = 2
            if lvl[myg+1][mxg+1] == 1: lvl[myg+1][mxg+1] = 115
            else: lvl[myg+1][mxg+1] = 2
            if lvl[myg+1][mxg] == 1: lvl[myg+1][mxg] = 116
            else: lvl[myg+1][mxg] = 2
            if lvl[myg+1][mxg-1] == 1: lvl[myg+1][mxg-1] = 117
            else: lvl[myg+1][mxg-1] = 2
            if lvl[myg][mxg-1] == 1: lvl[myg][mxg-1]   = 118
            else: lvl[myg][mxg-1] = 2
            lvl[myg][mxg] = modes[mode][item].id

    # Update
    # Draw
    screen.fill((0,0,0))
    
    screen.blit(selector.surf, (mxg*s+cam_x, myg*s+cam_y))
     
    for i in range(0, n):
        for j in range(0, n):
            if j*s+cam_y > MAXY: break
            screen.blit(quick[lvl[j][i]], (i*s+cam_x,j*s+cam_y))
        if i*s+cam_x > MAXX: break
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60)

