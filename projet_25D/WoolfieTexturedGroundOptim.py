#------------------------------------------------------------------------------
# Wolfenstein 3D raycasting engine recreation
# Inspired by Lode Vandevenne tutorials in C
# Damien Gouteux 2015
#------------------------------------------------------------------------------

import pygame
from pygame.locals import *
import math
import sys

screenWidth = 320  #300 #640
screenHeight = 240 #200 #480
texWidth = 64
texHeight = 64

WHITE = (255, 255, 255)

WALL_TEXTURED = True
FLOOR_TEXTURED = True
FPS = 60 #

#------------------------------------------------------------------------------
# Matrix & Area tools
#------------------------------------------------------------------------------

def debug(w, block=True):
    print(str(w))
    if block: raw_input()

def area(size, default):
    l = []
    for i in range(0,size):
        l.append(default)
    return l

def matrix(sizex, sizey, default):
    l = []
    for i in range(0,sizex):
        ll = area(sizey, default)
        l.append(ll)
    return l

def print_area(area):
    for i in range(0,len(area)):
        sys.stdout.write(str(area[i]))
        if i != len(area)-1: sys.stdout.write(',')
    sys.stdout.write("\n")
    sys.stdout.flush()

def print_matrix(matrix):
    for i in range(0,len(matrix)):
        print_area(matrix[i])

es1 = area(3, 'a')
es2 = matrix(3, 3, 'b')
print_area(es1)
print_matrix(es2)

#------------------------------------------------------------------------------
# Texture Generator
#------------------------------------------------------------------------------

tex = area(8, None)
for i in range(0,8):
    tex[i] = area(texWidth * texHeight, 0)

# Generate some textures

for x in range(0, texWidth):
    for y in range(0, texHeight):
        c_xor = int(x * 256 / texWidth) ^ int(y * 256 / texHeight)
        c_y = y * 256 / texHeight
        c_xy = y * 128 / texHeight + x * 128 / texWidth
        # flat red texture with black cross        
        tex[0][texWidth * y + x] = 65536*254*(x!=y and x != texWidth - y)
        # sloped greyscale
        tex[1][texWidth * y + x] = c_xy + 256 * c_xy + 65536 * c_xy
        # sloped yellow gradient
        tex[2][texWidth * y + x] = 256 * c_xy + 65536 * c_xy
        # xor greyscale
        tex[3][texWidth * y + x] = c_xor + 256 * c_xor + 65536 * c_xor
        # xor green 
        tex[4][texWidth * y + x] = 256 * c_xor
        # red bricks
        tex[5][texWidth * y + x] = 65536 * 192 * (x % 16 and y % 16)
        # red gradient
        tex[6][texWidth * y + x] = 65536 * c_y
        # flat grey texture
        tex[7][texWidth * y + x] = 128 + 256 * 128 + 65536 * 128

#------------------------------------------------------------------------------
# Texture Handling
#------------------------------------------------------------------------------

def load_texture(filename, where):
    global tex
    # Load
    s = pygame.image.load(filename)
    z = area(texWidth * texHeight, 0)
    xxx = 0
    #print(s.get_height())
    #print(s.get_width())
    for ii in range(0, s.get_height()):
        for jj in range(0, s.get_width()):
            t = tuple(s.get_at((jj,ii)))
            z[xxx] = t[0] * 256 * 256 + t[1] * 256 + t[2]
            xxx+=1
            #print("%s for %s" % (z[xxx-1],xxx-1))
    tex[where] = z

load_texture('textures/eagle.png', 0)
load_texture('textures/wood.png', 1)
load_texture('textures/redbrick.png', 2)
load_texture('textures/bluestone.png', 3)
load_texture('textures/greystone.png', 4) # pb quand on applique le filtre "dark side"

#------------------------------------------------------------------------------
# Main loop
#------------------------------------------------------------------------------

pygame.init()
pygame.display.set_caption('Woolfie 3D')
resolution = (640, 480)
flags = pygame.DOUBLEBUF # | pygame.FULLSCREEN

print(pygame.display.mode_ok(resolution))
# 0 : not ok
# !0: best color depth

screen = pygame.display.set_mode(resolution,flags,32)
sbuffer = pygame.Surface((screenWidth, screenHeight))

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

pygame.key.set_repeat(1,50)
default = pygame.font.SysFont(pygame.font.get_default_font(), 16)

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

def reboot():
    global position, direction, camera
    position = [22.0,12.0]
    direction = [-1.0,0.0]
    camera = [0.0, 0.66]

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
        elif event.type == KEYDOWN and event.key == K_SPACE:
            reboot()
        elif event.type == KEYUP and event.key == K_w:
            WALL_TEXTURED = not WALL_TEXTURED
        elif event.type == KEYUP and event.key == K_f:
            FLOOR_TEXTURED = not FLOOR_TEXTURED
        elif event.type == KEYUP and event.key == K_b:
            if screenWidth == 320:
                screenWidth = 640
                screenHeight = 480
            else:
                screenWidth = 320
                screenHeight = 240
            sbuffer = pygame.Surface((screenWidth, screenHeight))
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
    
    screen.blit(default.render(" x = %f  y = %f" % (position[0], position[1]), True, (255,0,0)), (320, 260))
    screen.blit(default.render("dx = %f dy = %f" % (direction[0], direction[1]), True, (0,255,0)), (320, 278)) #260+16+2))
    screen.blit(default.render("cx = %f cy = %f" % (camera[0], camera[1]), True, (0,0,255)), (320, 296)) #260+18*2))
    screen.blit(default.render("Press space to reboot simulation", True, WHITE), (320, 314)) #260+18*3))
    screen.blit(default.render("Press escape to quit", True, WHITE), (320, 332)) #260+18*4))
    screen.blit(default.render("Press w to switch wall texturing", True, WHITE), (320, 350)) #260+18*5))
    screen.blit(default.render("Press f to switch floor texturing", True, WHITE), (320, 368))
    screen.blit(default.render("Press b to display on 640x480 (b again to reset to 300x200)", True, WHITE), (320, 386)) #260+18*6))
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
    
    if not FLOOR_TEXTURED:
        sbuffer.fill((64, 64, 64), (0, 0, screenWidth, screenHeight/2))
        sbuffer.fill((128, 128, 128), (0, screenHeight/2, screenWidth, screenHeight/2))

    if WALL_TEXTURED or FLOOR_TEXTURED:
        buffer = pygame.PixelArray(sbuffer) ##
        
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
        
        ## DEB TEXTURE
        
        if WALL_TEXTURED or FLOOR_TEXTURED:
        
            # texturing calculations
            # 1 subtracted from it so that texture 0 can be used!
            texNum = area[mapX][mapY] - 1
        
            # calculate value of wallX
            wallX = 0.0 # where exactly the wall was hit
            if side == 1:
                wallX = rayPosX + ((mapY - rayPosY + (1 - stepY) / 2) / rayDirY) * rayDirX
            else:
                wallX = rayPosY + ((mapX - rayPosX + (1 - stepX) / 2) / rayDirX) * rayDirY
            wallX -= math.floor(wallX)
        
        if WALL_TEXTURED:
        
            # x coordinate on the texture
            texX = int(wallX * float(texWidth))
            
            if side == 0 and rayDirX > 0: texX = texWidth - texX - 1
            if side == 1 and rayDirY < 0: texX = texWidth - texX - 1
            
            # ME BICOLOR TEXTURE
            # if texX > 32: color = ((color[0]+100)%255,color[1],color[2])

            ## ME Now y
            for yy in range(drawStart, drawEnd):
                dd = yy * 256 - height * 128 + lineHeight * 128 # 256 and 128 factors to avoid floats
                texY = int(((dd * texHeight) / lineHeight) / 256) # Py3.x error : it must be an int and not a float
                # ME Hum... Normalement les textures font 64 !!!
                if texY < 0 or texY > 63:
                    if texY < 0:
                        texY = 64 + texY
                    else:
                        texY = texY & 63
                # get pixel color from texture
                # make color darker for y-sides: R, G and B byte each divided through two with a "shift" and an "and"              
                try:
                    pixel = tex[texNum][int(texHeight * texY + texX)]
                except IndexError: # Py3.0 no need now
                    print("Texture error")
                    print("index = " + str(texNum) + " on " + str(len(tex)))
                    print("index = " + str(int(texHeight * texY + texX)) + " on " + str(len(tex[texNum])))
                    print("texX = " + str(texX) + " texY = " + str(texY))
                if side == 1: pixel = (int(pixel) >> 1) & 8355711
                try:
                    buffer[s, yy] = int(pixel)  # buffer.set_at((s,yy), int(pixel)) # Py3.0 pixel was promoted to float. It must be int!
                except TypeError: # Py3.0 no need now
                    print("Color ERROR : " + str(pixel))
            
        if FLOOR_TEXTURED:
            
            ##DEB FLOOR
                
            # FLOOR CASTING
            floorXWall = 0.0
            floorYWall = 0.0 # x, y position of the floor texel at the bottom of the wall

            # 4 different wall directions possible
            if side == 0 and rayDirX > 0:
                floorXWall = mapX
                floorYWall = mapY + wallX
            elif side == 0 and rayDirX < 0:
                floorXWall = mapX + 1.0
                floorYWall = mapY + wallX
            elif side == 1 and rayDirY > 0:
                floorXWall = mapX + wallX
                floorYWall = mapY
            else:
                floorXWall = mapX + wallX
                floorYWall = mapY + 1.0
      
            distWall = 0.0
            distPlayer = 0.0
            currentDist = 0.0  

            distWall = perpWallDist
            distPlayer = 0.0

            if drawEnd < 0: drawEnd = height  #becomes < 0 when the integer overflows
      
            # draw the floor from drawEnd to the bottom of the screen
            for yyy in range(int(drawEnd + 1), height):
                currentDist = height / (2.0 * yyy - height) # you could make a small lookup table for this instead

                weight = (currentDist - distPlayer) / (distWall - distPlayer)
         
                currentFloorX = weight * floorXWall + (1.0 - weight) * position[0]
                currentFloorY = weight * floorYWall + (1.0 - weight) * position[1]
        
                floorTexX = 0
                floorTexY = 0
                
                floorTexX = int(currentFloorX * texWidth) & (texWidth-1)
                floorTexY = int(currentFloorY * texHeight) & (texHeight-1)
                
                ## Checkboard pattern
                checkerBoardPattern = (int(currentFloorX) + int(currentFloorY)) & 1
                floorTexture = 0
                if checkerBoardPattern == 0: floorTexture = 3
                else: floorTexture = 4 #6
                ##
                
                # floor and celing (symmetrical)
                buffer[s,yyy] =  (tex[floorTexture][texWidth * floorTexY + floorTexX] >> 1) & 8355711  # buffer.set_at((s,yyy), (tex[floorTexture][texWidth * floorTexY + floorTexX] >> 1) & 8355711)
                buffer[s, height-yyy] = tex[floorTexture][texWidth * floorTexY + floorTexX]  # buffer.set_at((s, height-yyy), tex[floorTexture][texWidth * floorTexY + floorTexX])

            ##END FLOOR
        
        ## END TEXTURE
        
        #UNTEX
        if not WALL_TEXTURED:
            pygame.draw.line(sbuffer, color, (s,drawStart), (s,drawEnd), 1)  ##
        
    if WALL_TEXTURED or FLOOR_TEXTURED:
        # From PyGame documentation:
        # During its lifetime, the PixelArray locks the surface, thus you explicitly have to delete it once its not used anymore and the surface should perform operations in the same scope.
        del buffer ##
    screen.blit(sbuffer, (0,0))  ##
    sbuffer.fill((0,0,0))  ##
    
    pygame.display.flip()
    
    # Limit to 60 fps maximum
    clock.tick(FPS)

