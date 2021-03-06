# -*- coding: utf-8 -*-

# Import
import pygame
from pygame.locals import *

# Init
pygame.init()

pygame.display.set_caption('STR')

# Les grandes valeurs
MAP_X = 3200
MAP_Y = 3200

CAM_X = 0
CAM_Y = 0

RES_X = 800
RES_Y = 600

SCROLL_SENSIVITY = 10
SCROLL_SPEED = 5

FPS = 60

resolution = (RES_X, RES_Y) #(1600,900)
flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
color_depth = pygame.display.mode_ok(resolution)

if color_depth == 0:
    exit(1, "bad screen size")

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

Black = (0, 0, 0, 255)
White = (255, 255, 255, 255)
Red = (255, 0, 0, 255)
Green = (0, 255, 0, 255) 
Blue = (0, 0, 255, 255)
Yellow = (255, 255, 0, 255)

import math
def distance(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x**2+y**2)

def vec(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    d = distance(x1, y1, x2, y2)
    return (x/d, y/d)

class Thing:
    
    def __init__(self, player, x, y, size, vie=100):
        self.player = player
        self.x = x
        self.y = y
        self.mx = x
        self.my = y
        self.s = size
        self.waypoints = []
        self.targets = []
        self.vie = vie
    
    def do(self):
        global background
        old = (self.mx, self.my)
        if len(self.waypoints) != 0:
            v = vec(self.mx, self.my, self.waypoints[0][0], self.waypoints[0][1])
            print v
            self.mx = self.mx+v[0]
            self.my = self.my+v[1]
            
            """
            if self.x < self.waypoints[0][0]:
                self.x += 1
            elif self.x > self.waypoints[0][0]:
                self.x -= 1
            if self.y < self.waypoints[0][1]:
                self.y += 1
            elif self.y > self.waypoints[0][1]:
                self.y -= 1
            """
            
            collide = None
            for t in things.all():
                if t == self:
                    continue
                if distance(t.mx, t.my, self.mx, self.my) <= t.s+self.s:
                    self.mx = old[0]
                    self.my = old[1]
                    collide = t
                    break
            
            self.x = int(self.mx)
            self.y = int(self.my)
            
            if self.x == self.waypoints[0][0] and self.y == self.waypoints[0][1]:
                self.waypoints = self.waypoints[1:]

class Group:
    def __init__(self, c):
        self.core = []
        self.c = c # Check on class. It must have a link function
    
    def add(self, o):
        if o.__class__ != self.c:
            raise Exception("Wrong Class")
        elif o in self.core:
            raise Exception("Already inside this group")
        #elif not hasattr(o, 'link'):
        #    raise Exception("No link function")
        self.core.append(o)
    
    def all(self):
        return self.core

PLAYER = 1

things = Group(Thing)
things.add(Thing(PLAYER, 10, 10, 10))
things.add(Thing(PLAYER, 30, 30, 15))
things.add(Thing(2, 100, 100, 20))

select = []

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

MOD_LSHIFT = False
MOD_DEPOSE = False

START_X = 0
START_Y = 0
REC = False

MOD_BACK = False

def ask():
    s = raw_input()
    return s

class Surf:
    Fill = 0
    
    def __init__(self, x=800, y=600, mother=None):
        if mother is None:
            self.surface = pygame.Surface((x,y))
        else:
            self.surface = mother
        self.font = pygame.font.SysFont("Arial", 12)
    
    def clear(self, c=(0,0,0)):
        self.surface.fill((0,0,0))
    
    def text(self, x, y, text, c=(255,255,0), antialias=True):
        s = self.font.render(text, antialias, c)
        self.surface.blit(s, (x, y))
    
    def get(self, x,y):
        global Black
        sx, sy = self.surface.get_size()
        if x < 0 or y < 0 or x >= sx or y >= sy:
            return Black
        return self.surface.get_at((x,y))
    
    def circle(self, x, y, r, c=(255, 255, 255), w=0):
        pygame.draw.circle(self.surface, c, (x, y), r, w)
    
    def send(self, x, y, s):
        if s.__class__ == pygame.Surface:
            s.blit(self.surface, (x, y))
        elif s.__class__ == Surf:
            s.surface.blit(self.surface, (x, y))
        else:
            raise Exception("Wrong type")
    
    def rect(self, x, y, h, w, c=(255,255,0), pencil=0):
        pygame.draw.rect(self.surface, c, (x, y, h, w), pencil)
    
    def line(self, x1, y1, x2, y2, c=(255,255,0), pencil=1):
        pygame.draw.line(self.surface, c, (x1, y1), (x2, y2), pencil)

screen = Surf(mother=screen)

def cx(x):
    global CAM_X
    return x-CAM_X

def cy(y):
    global CAM_Y
    return y-CAM_Y

def uncx(x):
    global CAM_X
    return x+CAM_X

def uncy(y):
    global CAM_Y
    return y+CAM_Y

# Main loop
while not escape:
    # Handle events
    for event in pygame.event.get():
        # Detect mod
        if event.type == KEYDOWN:
            if (event.mod & (KMOD_SHIFT | KMOD_LSHIFT)) or event.key == K_LSHIFT:
                MOD_LSHIFT = True
            elif event.key == K_TAB:
                MOD_BACK = True
        if event.type == KEYUP:
            if event.key == K_LSHIFT:
                MOD_LSHIFT = False
            elif event.key == K_e:
                MOD_DEPOSE = not MOD_DEPOSE
            elif event.key == K_TAB:
                MOD_BACK = False
        # Others
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
        # Mouse
        if event.type == MOUSEBUTTONUP:
            if event.button == MOUSE_LEFT:
                if MOD_DEPOSE:
                    things.add(Thing(1, event.pos[0], event.pos[1], 6))
                REC = False
                if not MOD_LSHIFT:
                    select = []
                x = uncx(event.pos[0])
                y = uncy(event.pos[1])
                min_x = min(x, START_X)
                min_y = min(y, START_Y)
                max_x = max(x, START_X)
                max_y = max(y, START_Y)
                for t in things.all():
                    if t.x >= min_x and t.x <= max_x and t.y >= min_y and t.y <= max_y or t.x + t.s >= min_x and t.x - t.s <= max_x and t.y + t.s >= min_y and t.y - t.s <= max_y:
                        select.append(t)
        if event.type == MOUSEBUTTONDOWN:
            print "event button = ", event.button
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
            elif event.button == MOUSE_LEFT:
                START_X = uncx(event.pos[0])
                START_Y = uncy(event.pos[1])
                REC = True
                print "True"
            elif event.button == MOUSE_RIGHT:
                p = (uncx(event.pos[0]), uncy(event.pos[1]))
                target = None
                for t in things.all():
                    if t.x - t.s <= p[0] and t.x + t.s >= p[0] and t.y - t.s <= p[1] and t.y + t.s >= p[1]:
                        target = t
                        break
                print target
                if target == None:
                    for s in select:
                        if MOD_LSHIFT:
                            s.waypoints.append(p)
                        else:
                            s.waypoints = [p]
                elif target.player != PLAYER:
                    # ATTACK
                    for s in select:
                        if MOD_LSHIFT:
                            s.targets.append(target)
                        else:
                            s.targets = [target]
            print "camx, camy, z, zoom[x]", camx, camy, z, zoom[z]
    camx -= modx
    camy -= mody
    
    # Update
    for t in things.all():
        t.do()
    
    # Draw
    # Features :
    #  Handle Scrolling
    #  Draw Rectangle selection
    #  Change View Filter (Background collision view)
    #  Draw Units (selected ones != not selected) and waypoints
    
    screen.clear()
    
    mx, my = pygame.mouse.get_pos()
    
    # Scrolling
    if mx <= 5 and CAM_X > 0:
        CAM_X -= SCROLL_SPEED
    elif mx >= RES_X - SCROLL_SENSIVITY and CAM_X < MAP_X - RES_X:
        CAM_X += SCROLL_SPEED
    if my <= 5 and CAM_Y > 0:
        CAM_Y -= SCROLL_SPEED
    elif my >= RES_Y - SCROLL_SENSIVITY and CAM_Y < MAP_Y - RES_Y:
        CAM_Y += SCROLL_SPEED
    
    # Draw Map
    for i in range(0, maxi):
        for j in range(0, maxj):
            screen.rect(cx(i*zoom[z]+camx), cy(j*zoom[z]+camy), zoom[z], zoom[z], Red, 1)
    
    # Rectangle selection
    if REC:
        min_x = min(mx, cx(START_X))
        min_y = min(my, cy(START_Y))
        max_x = max(mx, cx(START_X))
        max_y = max(my, cy(START_Y))
        screen.rect(min_x, min_y, max_x-min_x, max_y-min_y, Yellow, 1)
    
    # Draw Units (selected ones != not selected) and waypoints
    for t in things.all():
        x = cx(t.x)
        y = cy(t.y)
        s = t.s
        if t in select:
            screen.circle(x, y, s, Blue, Surf.Fill)
            if len(t.waypoints) != 0:
                last = (x, y)
                for p in t.waypoints:
                    px = cx(p[0])
                    py = cy(p[1])
                    screen.circle(px, py, 5, Blue, Surf.Fill)
                    screen.line(last[0], last[1], px, py, Blue, 1)
                    last = (px, py)
            if len(t.targets) != 0:
                last = (x, y)
                for t in t.targets:
                    px = cx(t.x)
                    py = cy(t.y)
                    screen.line(last[0], last[1], px, py, Red, 1)
        else:
            screen.circle(x, y, s, Green, Surf.Fill)
        screen.text(x-5, y-5, str(t.player))
    
    # View Filter (Background collision view)
    #if MOD_BACK:
    #    c = background.get(mx, my)
    #    background.send(0, 0, screen)
    #    screen.text(mx, my, str(c[0])+','+str(c[1])+','+str(c[2]))
    
    screen.text(10,10, str(CAM_X)+','+str(CAM_Y))
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(FPS)

print "Fin normale"
