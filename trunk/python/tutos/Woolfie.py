# http://www.cplusplus.com/reference/clibrary/cmath/fabs/
# http://www.student.kuleuven.be/~m0216922/CG/raycasting.html
# http://www.pygame.org/docs/tut/newbieguide.html
# http://www.permadi.com/tutorial/raycast/
#   http://www.permadi.com/tutorial/raycast/rayc8.html distorsion

# Import
import pygame
from pygame.locals import *

import math

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
camera = [0, 0.66]      # camera plane (orthogonal to direction vector) 2 * atan(0.66/1.0)=66

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
    
    # Raytracing
    height = 100
    width = 200
    for s in range(0, width):
        cameraX = 2 * s / float(width) - 1 #x-coordinate in camera space
        rayPosX = position[0]
        rayPosY = position[1]
        rayDirX = direction[0] + camera[0] * cameraX
        rayDirY = direction[1] + camera[1] * cameraX
        
        # #
        # which box of the map we're in  
        mapX = int((rayPosX-200)/10);
        mapY = int((rayPosY-200)/10);
        
        # length of ray from current position to next x or y-side
        sideDistX = 0.0
        sideDistY = 0.0
        
        # Ajout perso
        if rayDirX == 0: rayDirX = 0.00001
        if rayDirY == 0: rayDirY = 0.00001
        
        #length of ray from one x or y-side to next x or y-side
        deltaDistX = math.sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
        deltaDistY = math.sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
        perpWallDist = 0.0
       
        # what direction to step in x or y-direction (either +1 or -1)
        stepX = 0
        stepY = 0
        
        hit = 0 # was there a wall hit?
        side = 0 # was a NS or a EW wall hit?
        
        # #
        # calculate step and initial sideDist
        if rayDirX < 0:
            stepX = -1
            sideDistX = (rayPosX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - rayPosX) * deltaDistX
        if rayDirY < 0:
            stepY = -1
            sideDistY = (rayPosY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - rayPosY) * deltaDistY
        
        # perform DDA
        while hit == 0:
            # jump to next map square, OR in x-direction, OR in y-direction
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1
            # Check if ray has hit a wall
            #print mapX
            #print mapY
            if area[mapX][mapY] > 0: hit = 1
        
        # Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
        if side == 0:
            perpWallDist = abs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX) # fabs
        else:
            perpWallDist = abs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY) # fabs
        
        # Calculate height of line to draw on screen
        lineHeight = abs(int(height / perpWallDist))
       
        # Calculate lowest and highest pixel to fill in current stripe
        drawStart = -lineHeight / 2 + height / 2
        if drawStart < 0: drawStart = 0
        drawEnd = lineHeight / 2 + height / 2
        if drawEnd >= height: drawEnd = height - 1
        
        pygame.draw.line(screen, (255, 255, 0), (s,drawStart), (s,drawEnd), 1)
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(60) 
