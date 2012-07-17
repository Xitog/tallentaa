#! /usr/bin/env python

# http://ezide.com/games/code_examples/example.py
# http://pygame.org/docs/ref/draw.html#pygame.draw.rect

# div X et Y / 32 -> donne le carre ou on est.
# remultiplie par 32 -> donne la ou on commence a afficher

import pygame, sys, math
from pygame.locals import *

pygame.init()
size = width, height = 800, 600 #320, 240
screen = pygame.display.set_mode(size)

class Particles:
    def __init__(self):
        self.core = []
    
    def add(self, p):
        self.core.append(p)
    
    def update(self):
        i = 0
        while i < len(self.core):
            ttl = self.core[i].update()
            if ttl <= 0:
                del self.core[i]
                print ttl, len(self.core)
            else:
                i+=1
                print ttl, len(self.core)

class Particle:
    def __init__(self, pos, dir, target, ttl, guided=False):
        self.x = pos[0]
        self.y = pos[1]
        self.ax = dir[0]
        self.ay = dir[1]
        self.vel = dir[2]
        self.tx = target[0]
        self.ty = target[1]
        self.ttl = ttl
        self.guided = guided
    
    def update(self):
        if self.ttl == 0:
            return 0
        if not self.guided:
            self.x += self.vel*self.ax
            self.y += self.vel*self.ay
        else:
            pass
        #print self.x > self.tx and self.y > self.ty
        if self.x > self.tx and self.y > self.ty:
            self.ttl = 0
        else:
            self.ttl -= 1
        return self.ttl

class World:
    def __init__(self):
        self.particles = Particles()

world = World()

#-----------------------------------------------------------------------
# Scrolling

X = 0
Y = 0

left = False
right = False
up = False
down = False

SCROLL_MOD = 5

#-----------------------------------------------------------------------
# Selection

SELECT_X = 0
SELECT_Y = 0
SELECT_R = False

add_mod = False

units = []
selected = []

#MAX_VIEW_X = 10
#MAX_VIEW_Y = 8

#-----------------------------------------------------------------------

class Order:
    
    def __init__(self, kind=None, x=0, y=0, target=None):
        self.x = (x/32*32)+16
        self.y = (y/32*32)+16
        self.target = target
        self.kind = kind

#-----------------------------------------------------------------------

class Unit:
    
    def __init__(self, side, x, y, size, range, life, dom, reload=50, world=None):
        self.side = side
        self.x = (x/32*32)+16
        self.y = (y/32*32)+16
        self.size = size
        self.orders = []
        self.range = range
        self.life = life
        self.dom = dom
        self.reload = reload
        self.cpt = 0
        self.world = world
    
    def update(self):
        #print 'update ', len(self.orders)
        if self.life <= 0:
            return False
        
        if len(self.orders) > 0:
            o = self.orders[0]
            if o.kind == 'go':
                r = self.go(o.x, o.y)
                if r: del self.orders[0]
            elif o.kind == 'attack':
                #print o.kind, o.target, o.target.x, o.target.y
                if math.sqrt((self.x-o.target.x)**2 + (self.y-o.target.y)**2) > self.range or (self.x-16) % 32 != 0 or (self.y-16) % 32 != 0:
                    self.go(o.target.x, o.target.y)
                elif self.cpt <= 0:
                    world.particles.add(Particle([self.x,self.y], [1, 1, 4], [o.target.x, o.target.y], self.range+10, False))
                    o.target.life -= self.dom
                    self.cpt = self.reload
                    if o.target.life <= 0:
                        del self.orders[0]
                else:
                    self.cpt -= 1
        return True
    
    def order(self, o):
        #print 'order'
        self.orders = [o]
    
    def add_order(self, o):
        self.orders.append(o)
    
    def go(self, x, y):
        # 32 en 32
        from_x32 = self.x/32
        from_y32 = self.y/32
        to_x32 = x/32
        to_y32 = y/32
        
        #print 'dest x,y = ', x,y
        #print 'dest32 x,y = ', to_x32, to_y32
        
        if to_x32 > from_x32: n_x32 = from_x32+1
        elif to_x32 < from_x32: n_x32 = from_x32 - 1
        elif to_x32 == from_x32: n_x32 = from_x32
        if to_y32 > from_y32: n_y32 = from_y32+1
        elif to_y32 < from_y32: n_y32 = from_y32 - 1
        elif to_y32 == from_y32: n_y32 = from_y32
        
        x = n_x32 * 32 + 16
        y = n_y32 * 32 + 16
        ##
        
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
        return self.x == x and self.y == y

#-----------------------------------------------------------------------
# Tools

def xrect(x1, y1, x2, y2):
    tx = abs(x1-x2)
    ty = abs(y1-y2)
    if x1 > x2:
        rx = x2
    else:
        rx = x1
    if y1 > y2:
        ry = y2
    else:
        ry = y1
    return Rect(rx, ry, tx, ty)

def select(x, y):
    global units
    for u in units:
        if x >= u.x-u.size and x <= u.x + u.size and y >= u.y-u.size and y <= u.y+u.size:
            return u
    return False

#-----------------------------------------------------------------------
# Current setting

my_map = [
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

print 'mapX :', len(my_map[0])
print 'mapY :', len(my_map)

MAP_X = 32
MAP_Y = 32

side1 = Color(255, 255, 0)
side2 = Color(0, 255, 255)

SIDE_PLAYER = side1

units.append(Unit(side1, 10, 10, size=10, range=100, life=100, dom=5, world=world))
units.append(Unit(side1, 32, 32, size=10, range=150, life=100, dom=10, world=world))
units.append(Unit(side2, 200,200,size=20, range=30, life=300, dom=20, world=world))

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
                print 'add_mod!'
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
                print 'stop add mod!'
            elif event.key == K_SPACE:
                SCROLL_MOD += 1
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if not SELECT_R:
                    SELECT_R = True
                    SELECT_X = mx-X
                    SELECT_Y = my-Y
        elif event.type == MOUSEBUTTONUP:
            SELECT_R = False
            if event.button == 1:
                if mx32 in range(0, MAP_X) and my32 in range(0, MAP_Y):
                    print 'map=', my_map[mx32][my32]
                if select(mx-X, my-Y):
                    u = select(mx-X, my-Y)
                    print 'unit=', u, 'life=', u.life
                    if add_mod:
                        print 'ajout'
                        selected.append(u)
                    else:
                        print 'redo'
                        selected = [u]
                else:
                    selected = []
            elif event.button == 3:
                print 'button 2'
                s = select(mx-X, my-Y)
                if not s:
                    for u in selected:
                        if not add_mod:
                            print 'set order!'
                            u.order(Order('go', mx-X, my-Y))
                        else:
                            print 'add order!'
                            print len(u.orders)
                            u.add_order(Order('go', mx-X, my-Y))
                            print len(u.orders)
                elif s.side != SIDE_PLAYER:
                    for u in selected:
                        if not add_mod:
                            u.order(Order('attack', target=s))
                        else:
                            u.add_order(Order('attack', target=s))
            elif event.button == 2:
                print 'button 3'
    
#-----------------------------------------------------------------------
# Update

    if left:
        X+=SCROLL_MOD
    if right:
        X-=SCROLL_MOD
    if down:
        Y-=SCROLL_MOD
    if up:
        Y+=SCROLL_MOD
    
    for u in units:
        if not u.update():
            units.remove(u)
            del u

    #for p in world.particles.core:
    #    p.update()
    world.particles.update()
    
#-----------------------------------------------------------------------
# Render
    
    #print X, Y
    
    screen.fill(Color(0, 0, 0, 255))
    
    for yy in range(0, MAP_Y):
        for xx in range(0, MAP_X):
            #sys.stdout.write(str(my_map[yy][xx]))
            r = my_map[yy][xx]
            if r == 1:
                pygame.draw.rect(screen, Color(255, 0, 0, 128), (xx*32+X, yy*32+Y, 32, 32), 1)
            else:
                pygame.draw.rect(screen, Color(0, 255, 0, 128), (xx*32+X, yy*32+Y, 32, 32), 1)
    
    if SELECT_R:
        r = xrect(SELECT_X+X, SELECT_Y+Y, mx, my)
        pygame.draw.rect(screen, Color(255, 255, 255, 255), r, 1)
    
    for u in units:
        if u in selected:
            c = Color(0, 0, 255, 255)
            if len(u.orders) > 0:
                lx = u.x
                ly = u.y
                for o in u.orders:
                    if o.kind == 'go':
                        pygame.draw.circle(screen, c, (o.x+X, o.y+Y), 5, 0)
                        pygame.draw.line(screen, c, (lx+X, ly+Y), (o.x+X, o.y+Y), 1)
                        lx = o.x
                        ly = o.y
                    elif o.kind == 'attack':
                        pygame.draw.circle(screen, Color(255,0,0), (o.target.x+X, o.target.y+Y), 5, 0)
                        pygame.draw.line(screen, Color(255,0,0), (lx+X, ly+Y), (o.target.x+X, o.target.y+Y), 1)
                        lx = o.target.x
                        ly = o.target.y
        else:
            c = u.side
        #    c = Color(0, 255, 0, 255)
        pygame.draw.circle(screen, c, (u.x+X, u.y+Y), u.size, 0)
    
    for p in world.particles.core:
        pygame.draw.circle(screen, Color(255,0,0), (p.x+X, p.y+Y), 3, 0)
    
    INTERFACE_Y = 480
    # Interface
    pygame.draw.rect(screen, Color(200, 200, 200), (0, INTERFACE_Y, 799, 200), 0)
    pygame.draw.line(screen, Color(0,0,255), (0, INTERFACE_Y), (799, INTERFACE_Y), 1)
    for xx in range(0,3):
        for yy in range(0,3):
            pygame.draw.rect(screen, Color(0, 0, 255), (xx*32, yy*32+INTERFACE_Y, 32, 32), 1)
    pygame.draw.line(screen, Color(0,0,255), (703, INTERFACE_Y), (703, INTERFACE_Y+96), 1)
    pygame.draw.line(screen, Color(0,0,255), (703, INTERFACE_Y+96), (799, INTERFACE_Y+96), 1)
    
    # fin Interface
    
    #screen.blit(ball, ballrect)
    pygame.display.flip()
    
    pygame.time.Clock().tick(60)


