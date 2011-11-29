# -*- coding: utf-8 -*-
# http://www.pygame.org/docs/
# http://docs.python.org/library/urllib.html

# Import
import pygame
from pygame.locals import *
import math # sqrt

# Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
FILL = 0
BLEND = 1
NOBLEND = 0
ALL = None

# Variables
title = 'Basic PyGame'
resolution = (800,600)
flags = pygame.DOUBLEBUF
colors = 32

# Init
pygame.init()
pygame.display.set_caption(title)

screen = pygame.display.set_mode(resolution, flags, colors)

escape = False
clock = pygame.time.Clock()

draw = pygame.Surface((300,300))
light = pygame.Surface((30,30))

x = 40
x2 = 200
y2 = 100

down = False

# Load and saving surfaces
s = None
try:
    s = pygame.image.load("simple.bmp").convert()
except pygame.error as e:
    s = pygame.Surface((10,10))
    s.fill((128, 128, 0))
    pygame.image.save(s, "simple.bmp")
    s = pygame.image.load("simple.bmp").convert()

itex = 300
itey = 300

class CircleMove:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.r = radius
        self.a = 0
        self.cpt = 0

    def move(self, o):
        self.cpt += 1
        self.cpt %=3
        if self.cpt != 0:
            return    
        o.x += math.cos(self.a) * self.r
        o.y += math.sin(self.a) * self.r
        self.a += self.speed
        old = self.a
        self.a %= 360
        if old > self.a:
            o.reboot()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
    def reboot(self):
        self.x = self.startx
        self.y = self.starty

c = CircleMove(400, 100, 20, 0.25)
p = Point(420, 100)

# Main loop
while not escape:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        elif event.type == KEYDOWN:
            print 'Unicode:', event.unicode
            print 'Key:', event.key
            print 'Mod:', event.mod
            down = True
        elif event.type == KEYUP:
            # pygame.mixer.music.load(filename) mp3 or Ogg
            # pygame.mixer.music.play(loops=0, start=0.0) loops=-1 = infinite
            # pygame.mixer.music.pause()
            # pygame.mixer.music.unpause()
            # pygame.mixer.music.fadeout(time) time in milliseconds. Blocking method.
            # pygame.mixer.music.queue(filename) add to the queue
            down = False
        elif event.type == VIDEORESIZE:
            print event.size
            print event.w
            print event.h
        elif event.type == MOUSEMOTION:
            print event.pos
            print event.rel
            print event.buttons
    
    # Update
    
    if down: print "a key is down"
        
    # Draw
    screen.fill((0,0,0))
    
    # Dessin de formes
    pygame.draw.rect(screen, RED, (10, 10, 20, 20), FILL)
    pygame.draw.rect(screen, BLUE, (20, 20, 60, 60), 1)
    pygame.draw.circle(screen, GREEN, (100,100), 20, 1)
    pygame.draw.line(screen, RED, (30, 30), (80,80), 3)
    pygame.draw.aaline(screen, BLUE, (100,100), (120,120), NOBLEND)

    # Bliting a surface
    screen.blit(s, (x2, y2))
    x2 += 1
    x2 %= 600
    if x2 == 0: x2 = 200
    y2 += 1
    y2 %= 200
    if y2 == 0: y2 = 100
    
    # Dessin sur une sous-surface
    draw.fill(GREY)
    pygame.draw.circle(draw, BLUE, (30, 30), 10, FILL)
    draw.set_alpha(32) # 255 opaque
    screen.blit(draw, (200, 200))    

    # Transparence et Mouvement
    light.fill(BLACK)
    light.set_colorkey(BLACK)
    light.set_alpha(128)
    pygame.draw.circle(light, GREEN, (15, 15), 10, FILL)
    screen.blit(light, (x, 40), ALL, BLEND_ADD)
    x += 1
    x %= 70

    # Vector
    i = 300
    j = 300
    v = 400
    w = 400
    vector = (v-i, w-j)
    norme = math.sqrt(vector[0]**2+vector[1]**2)
    normalized = (vector[0]/norme, vector[1]/norme)
    # X = |v|cos(o)
    # Y = |v|sin(o)
    # |v| = magnitude
    laserlen = 10
    laserprog = 2
    pygame.draw.line(screen, RED, (itex, itey), (itex+laserlen*normalized[0],itey+laserlen*normalized[1]), 2)
    itex = itex+laserprog*normalized[0]
    itey = itey+laserprog*normalized[1]
    if itex > 400: 
        itex=300
        itey=300
    # 16h09 OK

    # Mvt
    c.move(p)
    pygame.draw.circle(screen, BLUE, (p.x,p.y), 5, FILL)

    pygame.display.flip()

    # Limit to 60 fps maximum
    clock.tick(60)

