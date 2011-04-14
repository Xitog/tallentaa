# -*- coding: utf-8 -*-
# Dig!

# Import
import pygame
from pygame.locals import *

# Init
pygame.init()
pygame.display.set_caption('Dig Edit')

resolution = (800,600)
flags = pygame.DOUBLEBUF
screen = pygame.display.set_mode(resolution,flags,32)

escape = False
clock = pygame.time.Clock()

v = 0
n = 32
s = 32
lvl = [[v]*n for x in xrange(n)]

act = False

item = 'Water'
mode = 'Texture'

#

obj = {}

def init(source, **key):
    o = source.copy()
    o.update(key)
    if o.has_key('init'):
        o['init'](o)
    return o

def inherit(cls, xfrom):
    cls['super'] = xfrom
    #cls.update(xfrom)

#

def ini_texture(tex):
    tex['surf'] = pygame.image.load(tex['file']).convert()
    tex['surf'].set_colorkey((255,0,255))

Texture = {
    'name' : None,
    'file' : None,
    'id'   : None,
    'surf' : None,
    'init' : ini_texture
}
inherit(Texture, obj)

#

grass = init(Texture, name='Grass', file='basic.png', id='1')
water = init(Texture, name='Water', file='basic2.png', id='2')
selector = init(Texture, name='Selector', file='Selector.png', id='0')

#

textures = {
    'Grass' : 'basic.png',
    'Water' : 'basic2.png'
}

doodads = {
    'Desert Tree 1' : 'DesertTree1.png',
    'Desert Tree 2' : 'DesertTree2.png',
    'Desert Tree 3' : 'DesertTree3.png'
}

modes = {'Texture':textures, 'Doodad':doodads, 'Object': {}}

def make(myDic):
    for k in myDic:
        try:
            s = pygame.image.load(myDic[k]).convert()
            s.set_colorkey((255,0,255))
            i = hash(myDic[k])
            print 'Loaded ressource %s @%s' % (myDic[k],i)
            myDic[k] = (i, s)
        except pygame.error as e:
            print e

for k in modes:
    print '----> Loading %s' % (k,)
    make(modes[k])

def fromHash(myHash):
    global modes
    for k in modes:
        for i in modes[k]:
            if modes[k][i][0] == myHash:
                return modes[k][i][1]
    return modes['Texture']['Grass'][1]

print mode
print item

import sys

selector['surf'].set_alpha(192)

pygame.mouse.set_pos([100,100])

# Main loop
while not escape:
    
    m = pygame.mouse.get_pos()
    mx = m[0]
    my = m[1]
    mxg = m[0]/s
    myg = m[1]/s

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        if event.type == MOUSEMOTION:
            print m[0], m[1], m[0]/s, m[1]/s
        if event.type == MOUSEBUTTONDOWN:
            print event.button
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
            #p = event.pos
            #xp = p[0] / s
            #yp = p[1] / s
            #lvl[xp][yp] = modes[mode][item][0]
            lvl[mxg][myg] = modes[mode][item][0]

    # Update
    # Draw
    screen.fill((0,0,0))
    
    xm = m[0] / s
    ym = m[1] / s
    screen.blit(selector['surf'], (xm*s, ym*s))
     
    for i in range(0, n):
        for j in range(0, n):
            screen.blit(fromHash(lvl[i][j]), (i*s,j*s))
            #if lvl[i][j] == 0: screen.blit(b, (i*s,j*s)) #screen.pygame.draw.rect(screen, (255,0,0), (i*s, j*s, s, s), 1)
            #else: screen.blit(b2, (i*s,j*s))

    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60)

