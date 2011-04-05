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
            activate = 100
            level = 1
    
    # Draw
    screen.fill((0,0,0))
    
    radius = 40
    
    mx, my = pygame.mouse.get_pos()
    if mx > 400-radius and mx < 400+radius and my > 300-radius and my < 300+radius:
        color = RED
    else:
        color = BLUE
    pygame.draw.circle(screen, color, (400,300), radius, 5)
    wrote_at(screen, "mots", 400, 300)
    wrote_at(screen, "(1200)", 400, 300+17)
    
    if level > 0:
        dir = [(-1,0),(0,-1),(1,0),(0,1)]
        for i in range(0,4):
            pygame.draw.circle(screen, GREEN, (400+dir[i][0]*(100-activate), 300+dir[i][1]*(100-activate)), radius, 5)
            wrote_at(screen, str(i), 400+dir[i][0]*(100-activate), 300+dir[i][1]*(100-activate))
            if activate == 0: pygame.draw.line(screen, RED, (400+dir[i][0]*(100-radius), 300+dir[i][1]*(100-radius)), (400+dir[i][0]*radius,300+dir[i][1]*radius))
        if activate > 0: activate -= 1
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60) 
