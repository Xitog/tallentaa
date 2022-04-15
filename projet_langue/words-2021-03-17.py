# 18h50 : base de "words"

import pygame
from pygame.locals import *

# Init
pygame.init()
pygame.display.set_caption('Words')
resolution = (800,600)
flags = pygame.DOUBLEBUF
print(pygame.display.mode_ok(resolution)) # !0: best color depth
screen = pygame.display.set_mode(resolution,flags,32)
clock = pygame.time.Clock()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.SysFont(pygame.font.get_default_font(), 16)

def wrote_at(surface, text, x, y):
    global font
    s = font.render(text, True, (255,0,0))
    sx, sy = s.get_size()
    screen.blit(s, (int(x-sx/2), int(y-sy/2)))

activate = 0
level = 0

class Circle:
    def __init__(self, x, y, radius, color, text=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.on = False
    
    def collision(self, x, y):
        return x > self.x-self.radius and mx < self.x+self.radius and my > self.y-self.radius and my < self.y+self.radius
    
    def pos(self):
        return (self.x, self.y)

class GCircle(Circle):
    def __init__(self, x, y, radius, color, text=None, logic=None):
        Circle.__init__(self, x, y, radius, color, text)
        self.logic = logic        
        if self.logic is not None:
            self.logic.link(self)
    
    def on_click(self):
        if self.logic is not None:
            self.logic.start()
    
    def update(self):
        if self.logic is not None:
            self.logic.update()
    
    def draw(self, surface):
        if self.on:
            c = RED
        else:
            c = self.color
        pygame.draw.circle(surface, c, self.pos(), self.radius, 5)
        wrote_at(screen, self.text, self.x, self.y)
        wrote_at(screen, "(1200)", self.x, self.y+17)

class GLogic:
    def __init__(self):
        self.master = None
        self.started = False
        pass
    
    def link(self, master):
        self.master = master
    
    def start(self):
        self.started = True

class Deploy(GLogic):
    def __init__(self):
        GLogic.__init__(self)
        self.activate = 100
        self.level = 1
    
    def start(self):
        GLogic.start(self)
        self.activate = 100
        self.level = 1
    
    def update(self):
        if not self.started:
            return
        rad = self.master.radius
        act = self.activate
        x = self.master.x
        y = self.master.y
        if self.level > 0:
            dir = [(-1,0),(0,-1),(1,0),(0,1)]
            for i in range(0,4):
                pygame.draw.circle(screen, GREEN, (x+dir[i][0]*(100-act), y+dir[i][1]*(100-act)), rad, 5)
                wrote_at(screen, str(i), x+dir[i][0]*(100-act), y+dir[i][1]*(100-act))
                if self.activate == 0: 
                    pygame.draw.line(screen, RED, (x+dir[i][0]*(100-rad), y+dir[i][1]*(100-rad)), (x+dir[i][0]*rad,y+dir[i][1]*rad))
            if self.activate > 0: self.activate -= 1

c = GCircle(400, 300, 40, BLUE, "mots", Deploy())
d = GCircle(200, 300, 30, GREEN, "youpi", Deploy())

Gents = [c, d]

# Main loop
escape = False
while not escape:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            escape = True
        elif event.type == KEYDOWN and event.key == K_LEFT:
            modx = -1
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            modx = 1
        elif event.type == KEYDOWN and event.key == K_UP:
            mody = -1
        elif event.type == KEYDOWN and event.key == K_DOWN:
            mody = 1
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                modx = 0
            elif event.key == K_DOWN or event.key == K_UP:
                mody = 0
        elif event.type == MOUSEBUTTONUP:
            for g in Gents:
                if g.collision(event.pos[0],event.pos[1]):
                    g.on_click()
    
    # Draw
    screen.fill((0,0,0))
    
    mx, my = pygame.mouse.get_pos()
    for g in Gents:
        g.on = g.collision(mx, my)
        g.update()
        g.draw(screen)
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60) 
