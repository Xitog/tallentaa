# http://www.cplusplus.com/reference/clibrary/cmath/fabs/
# http://www.student.kuleuven.be/~m0216922/CG/raycasting.html
# http://www.pygame.org/docs/tut/newbieguide.html
# http://www.permadi.com/tutorial/raycast/
#   http://www.permadi.com/tutorial/raycast/rayc8.html distorsion

# Import
import pygame
from pygame.locals import *

import math

screenWidth = 320  #300 #640
screenHeight = 240 #200 #480
FPS = 60 #

#------------------------------------------------------------------------------
# Main loop
#------------------------------------------------------------------------------

# Init
pygame.init()

pygame.display.set_caption('Woolfie 3D')

resolution = (800,600)
flags = pygame.DOUBLEBUF

print(pygame.display.mode_ok(resolution))
# 0 : not ok
# !0: best color depth

screen = pygame.display.set_mode(resolution,flags,32)

#sprite1 = pygame.image.load('flower.png').convert()
#sprite1.set_colorkey((255,0,255))

clock = pygame.time.Clock()

escape = False

map_size = (24,24)

area = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,5,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,7,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

position = [22.0,12.0]      # position vector (point)
direction = [-1.0,0.0]      # direction vector
camera = [0.0, 0.66]        # camera plane (orthogonal to direction vector) 2 * atan(0.66/1.0)=66

modx = 0.0
mody = 0.0


def ccolor(index):
    color = (255, 255, 0)
    if index == 1:
        color = (255, 0, 0)
    elif index == 2:
        color = (0, 255, 0)
    elif index == 3:
        color = (0, 0, 255)
    elif index == 4:
        color = (255, 255, 255)
    elif index == 5:
        color = (120, 120, 120)
    elif index == 6:
        color = (120, 0, 120)
    elif index == 7:
        color = (0, 0, 120)
    return color


right = False
left = False
up = False
down = False
# Main loop
while not escape:

    frameTime = 0.10
    rotSpeed = frameTime * 3.0
    moveSpeed = frameTime * 5.0
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            escape = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            escape = True
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                right = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                right = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False
                    
    # rotate to the right
    if right:
        # both camera direction and camera plane must be rotated
        oldDirX = direction[0]
        direction[0] = direction[0] * math.cos(-rotSpeed) - direction[1] * math.sin(-rotSpeed)
        direction[1] = oldDirX * math.sin(-rotSpeed) + direction[1] * math.cos(-rotSpeed)
        oldPlaneX = camera[0]
        camera[0] = camera[0] * math.cos(-rotSpeed) - camera[1] * math.sin(-rotSpeed)
        camera[1] = oldPlaneX * math.sin(-rotSpeed) + camera[1] * math.cos(-rotSpeed)
    if left:
        # both camera direction and camera plane must be rotated
        oldDirX = direction[0]
        direction[0] = direction[0] * math.cos(rotSpeed) - direction[1] * math.sin(rotSpeed)
        direction[1] = oldDirX * math.sin(rotSpeed) + direction[1] * math.cos(rotSpeed)
        oldPlaneX = camera[0]
        camera[0] = camera[0] * math.cos(rotSpeed) - camera[1] * math.sin(rotSpeed)
        camera[1] = oldPlaneX * math.sin(rotSpeed) + camera[1] * math.cos(rotSpeed)
    if up:
        try:        
            if area[int(position[0] + direction[0] * moveSpeed)][int(position[1])] == False: position[0] += direction[0] * moveSpeed
            if area[int(position[0])][int(position[1] + direction[1] * moveSpeed)] == False: position[1] += direction[1] * moveSpeed
        except Exception as e:
            print(int(position[0] + direction[0] * moveSpeed))
            print(int(position[1] + direction[1] * moveSpeed))
            print(e)
    if down:
        if area[int(position[0] - direction[0] * moveSpeed)][int(position[1])] == False: position[0] -= direction[0] * moveSpeed
        if area[int(position[0])][int(position[1] - direction[1] * moveSpeed)] == False: position[1] -= direction[1] * moveSpeed
        
    # Draw
    screen.fill((0,0,0))
    
    #screen.blit(sprite1, (100, 100))
    
    # Map and player
    REPX = 320
    REPY = 10
    SIZE = 10
    for i in range(0, len(area)):
        line = area[i]
        for j in range(0, len(line)):
            rx = i * SIZE + REPX
            ry = (len(line) - j) * SIZE + REPY # Y AXIS INVERTED
            color = ccolor(line[j])
            pygame.draw.rect(screen, color, (rx,ry,SIZE,SIZE),0)
            pygame.draw.rect(screen, (0, 0, 0), (rx, ry, SIZE, SIZE), 1)

    pos_x = int(position[0]*SIZE + REPX)
    pos_y = map_size[1]*SIZE-int(position[1]*SIZE) + REPY # Y AXIS INVERTED
    pygame.draw.rect(screen, (255,0,0), (pos_x, pos_y, SIZE, SIZE), 0)    
    #screen.set_at((pos_x,pos_y), (255,0,0))
    dir_x = pos_x+SIZE/2+direction[0]*SIZE
    dir_y = pos_y+SIZE/2-direction[1]*SIZE # Y AXIS INVERTED
    pygame.draw.line(screen, (255,0,0), (pos_x+SIZE/2, pos_y+SIZE/2), (dir_x, dir_y), 1)

    # Raytracing 2.5D
    height = screenHeight
    width = screenWidth
    for s in range(0, width):
        # calculate ray position and direction 
        cameraX = 2 * s / float(width) - 1 #x-coordinate in camera space
        rayPosX = position[0]
        rayPosY = position[1]
        rayDirX = direction[0] + camera[0] * cameraX
        rayDirY = direction[1] + camera[1] * cameraX
        
        # which box of the map we're in  
        mapX = int(rayPosX);
        mapY = int(rayPosY);
        
        # length of ray from current position to next x or y-side
        sideDistX = 0.0
        sideDistY = 0.0
        
        # Added by me. Is it still useful?
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
            if area[mapX][mapY] > 0: hit = 1
        
        # Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
        if side == 0:
            perpWallDist = abs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX) # fabs
        else:
            perpWallDist = abs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY) # fabs
        
        # Calculate height of line to draw on screen
        lineHeight = abs(int(float(height) / float(perpWallDist)))
       
        # Calculate lowest and highest pixel to fill in current stripe
        drawStart = int(-lineHeight / 2 + height / 2)
        if drawStart < 0: drawStart = 0
        drawEnd = int(lineHeight / 2 + height / 2)
        if drawEnd >= height: drawEnd = height - 1
        
        # choose wall color
        color = ccolor(area[mapX][mapY])
        pygame.draw.line(screen, (255, 255, 0), (s,drawStart), (s,drawEnd), 1)
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(FPS)

