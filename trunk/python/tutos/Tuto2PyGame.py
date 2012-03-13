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

sprite1 = pygame.image.load('flower.png').convert()
sprite1.set_colorkey((255,0,255))

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

# Main loop
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
    
    # Update
    position[0] += modx
    position[1] += mody
    
    # Draw
    screen.fill((0,0,0))
    
    screen.blit(sprite1, (100, 100))
    
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
