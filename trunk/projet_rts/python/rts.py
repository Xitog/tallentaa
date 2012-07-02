#! /usr/bin/env python

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X et Y / 32 -> donne le carre ou on est.
# remultiplie par 32 -> donne la ou on commence a afficher

import pygame, sys, math
from pygame.locals import *

pygame.init()
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

#-----------------------------------------------------------------------
# Scrolling

X = 0
Y = 0

left = False
right = False
up = False
down = False

SCROLL_MOD = 1

#-----------------------------------------------------------------------
# Selection

add_mod = False

units = []
selected = []

#MAX_VIEW_X = 10
#MAX_VIEW_Y = 8

#-----------------------------------------------------------------------

class Order:
    
    def __init__(self, kind=None, x=None, y=None, target=None):
        self.x = x
        self.y = y
        self.target = target
        self.kind = kind

#-----------------------------------------------------------------------

class Unit:
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.orders = []
    
    def update(self):
        #print 'update ', len(self.orders)
        if len(self.orders) > 0:
            o = self.orders[0]
            #print o.kind
            if o.kind == 'go':
                self.go(o.x, o.y)
    
    def order(self, o):
        #print 'order'
        self.orders = [o]
    
    def go(self, x, y):
        nx = self.x
        ny = self.y
        
        #print 'go', x, y, 'from', self.x, self.y
        if x > self.x: nx += 1
        elif x < self.x: nx -= 1
        if y > self.y : ny += 1
        elif y < self.y: ny -= 1
        
        coll = False
        for u in units:
            if u == self: continue
            distance = math.sqrt((u.x-nx)**2 + (u.y-ny)**2)
            if distance < self.size + u.size:
                coll = True 
                break
        if not coll:
            self.x = nx
            self.y = ny

#-----------------------------------------------------------------------
# Tools

def select(x, y):
    global units
    for u in units:
        if x >= u.x-u.size and x <= u.x + u.size and y >= u.y-u.size and y <= u.y+u.size:
            return u
    return False

#-----------------------------------------------------------------------
# Current setting

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

units.append(Unit(10, 10, 10))
units.append(Unit(30, 30, 10))
units.append(Unit(200,200,20))

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
            elif event.key == K_LSHIFT:
                add_mod = True
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                down = False
            elif event.key == K_UP:
                up = False
            elif event.key == K_LEFT:
                left = False
            elif event.key == K_RIGHT:
                right = False
            elif event.key == K_LSHIFT:
                add_mod = False
            elif event.key == K_SPACE:
                SCROLL_MOD += 1
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if mx32 in range(0, MAP_X) and my32 in range(0, MAP_Y):
                    print my_map[mx32][my32]
                if select(mx-X, my-Y):
                    u = select(mx-X, my-Y)
                    print u
                    if add_mod:
                        selected.append(u)
                    else:
                        selected = [u]
                else:
                    selected = []
            elif event.button == 3:
                print 'button 2'
                for u in selected:
                    u.order(Order('go', mx-X, my-Y))
            elif event.button == 2:
                print 'button 3'
    
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
    
    for u in units:
        u.update()

        if u in selected:
            c = Color(0, 0, 255, 255)
            if len(u.orders) > 0:
                if u.orders[0].kind == 'go':
                    pygame.draw.circle(screen, c, (u.orders[0].x+X, u.orders[0].y+Y), 5, 0)
                    pygame.draw.line(screen, c, (u.x+X, u.y+Y), (u.orders[0].x+X, u.orders[0].y+Y), 1)
        else:
            c = Color(0, 255, 0, 255)
        pygame.draw.circle(screen, c, (u.x+X, u.y+Y), u.size, 0)
        
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


